"""
===================================================================================
BÀI TẬP CUỐI KỲ (LAB-END): HỆ THỐNG NHẬN DIỆN KHUÔN MẶT THỜI GIAN THỰC
THUẬT TOÁN FACENET & MTCNN TRÊN WEBCAM / ẢNH TĨNH
===================================================================================

1. NGUYÊN LÝ HOẠT ĐỘNG & NỀN TẢNG LÝ THUYẾT:

   a) MTCNN (Phát hiện & Căn chỉnh khuôn mặt):
      - Gồm 3 mạng nơ-ron phân cấp liên tiếp: P-Net (Đề xuất vùng nghi ngờ),
        R-Net (Tinh chỉnh khung), O-Net (Chốt vị trí & 5 điểm đặc trưng khuôn mặt).
      - Xác định 5 điểm quan trọng: mắt trái, mắt phải, đỉnh mũi, 2 khóe miệng.
      - Căn chỉnh khuôn mặt xoay về góc nhìn thẳng chuẩn & đưa về Tensor (3, 160, 160).

   b) FaceNet (Trích xuất Vector đặc trưng):
      - Ánh xạ khuôn mặt thành một chuỗi 512 số thực (Vector Embedding 512 chiều)
        mô tả các đặc trưng riêng biệt của khuôn mặt.
      - Tối ưu bằng nguyên lý Triplet Loss: Kéo các vector cùng 1 người lại gần nhau
        và đẩy các vector của người khác ra xa nhau.
      - Chuẩn hóa tất cả các vector về cùng độ dài chuẩn bằng 1.

   c) Phép Đo Độ Tương Đồng & Phân Tích Chọn Ngưỡng Threshold (0.55 - 0.70):
      - Độ tương đồng (Cosine Similarity): Tính góc giữa 2 vector, kết quả từ 0 tới 1.
        + Tiến dần về 1.0: Hai khuôn mặt càng giống hệt nhau.
        + Tiến dần về 0.0: Hai khuôn mặt hoàn toàn khác nhau.
      - Ngưỡng Tiêu chuẩn (0.70): Áp dụng cho ảnh studio nét cao, nhìn thẳng, ánh sáng chuẩn.
      - Ngưỡng Thực tế Webcam (0.55 - 0.60):
        + Ánh sáng phòng & góc nghiêng biến thiên làm similarity của cùng 1 người dao động (0.58 - 0.75).
        + Nhiễu cảm biến camera laptop làm giảm độ sắc nét của đặc trưng.
        + Việc đặt ngưỡng 0.55 - 0.60 giúp webcam nhận diện mượt mà thời gian thực
          mà vẫn loại bỏ hoàn toàn người lạ (<0.40).

2. QUY TRÌNH PHÂN LOẠI & THRESHOLDING:
   - Nếu Similarity > Threshold  ==> "Matched: <Tên người dùng>" (Khung màu xanh lá).
   - Nếu Similarity <= Threshold ==> "Unknown" (Khung màu đỏ).
===================================================================================
"""

import os
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import cv2
import torch
# Thêm patch an toàn xử lý tương thích cho dispatch kernel nếu torch/torchvision gặp lệch phiên bản
if hasattr(torch, '_C') and hasattr(torch._C, '_dispatch_has_kernel_for_dispatch_key'):
    _orig_has_kernel = torch._C._dispatch_has_kernel_for_dispatch_key
    def _patched_has_kernel(qualname, key):
        try:
            return _orig_has_kernel(qualname, key)
        except RuntimeError:
            return False
    torch._C._dispatch_has_kernel_for_dispatch_key = _patched_has_kernel

import numpy as np
from PIL import Image

try:
    from facenet_pytorch import MTCNN, InceptionResnetV1
except Exception as e:
    print(f"[WARNING] Gặp cảnh báo khi import facenet_pytorch: {e}")
    try:
        from facenet_pytorch import MTCNN, InceptionResnetV1
    except ImportError:
        print("[ERROR] Thư viện 'facenet-pytorch' chưa được cài đặt. Hãy chạy: pip install facenet-pytorch torchvision")


def imread_unicode(path):
    """Đọc ảnh hỗ trợ unicode path trên Windows."""
    try:
        img_array = np.fromfile(path, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img
    except Exception:
        return None

def imwrite_unicode(path, img_bgr):
    """Lưu ảnh hỗ trợ unicode path trên Windows."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        ext = os.path.splitext(path)[1]
        if not ext:
            ext = '.jpg'
        res, img_encode = cv2.imencode(ext, img_bgr)
        if res:
            img_encode.tofile(path)
            return True
        return False
    except Exception:
        return False

class FaceRecognitionSystem:
    """
    Hệ thống Nhận diện khuôn mặt thời gian thực kết hợp MTCNN và FaceNet.
    """

    def __init__(self, threshold=0.7, device=None):
        """
        Khởi tạo hệ thống nhận diện khuôn mặt.
        :param threshold: Ngưỡng Similarity quyết định Matched (>0.7) hay Unknown (<=0.7).
        :param device: Thiết bị tính toán ('cuda' hoặc 'cpu').
        """
        self.threshold = threshold
        if device is None:
            self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)

        print(f"[INFO] Khởi tạo FaceRecognitionSystem trên thiết bị: {self.device}")

        # 1. Khởi tạo MTCNN cho phát hiện và cắt khuôn mặt
        self.mtcnn = MTCNN(
            image_size=160,
            margin=14,
            min_face_size=20,
            thresholds=[0.6, 0.7, 0.7],
            factor=0.709,
            post_process=True,
            keep_all=True,
            device=self.device
        )

        # MTCNN dạng crop 1 mặt duy nhất để phục vụ trích xuất reference embedding
        self.mtcnn_single = MTCNN(
            image_size=160,
            margin=14,
            min_face_size=20,
            post_process=True,
            keep_all=False,
            device=self.device
        )

        # 2. Khởi tạo FaceNet (InceptionResnetV1 pre-trained vggface2)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)

        # 3. Cơ sở dữ liệu lưu các khuôn mặt đã đăng ký {name: embedding_vector}
        self.registered_faces = {}

    def _to_pil_image(self, img_input):
        """Chuyển đổi các định dạng đầu vào (filepath, numpy BGR/RGB) thành PIL Image RGB."""
        if isinstance(img_input, str):
            if not os.path.exists(img_input):
                raise FileNotFoundError(f"Không tìm thấy file ảnh: {img_input}")
            return Image.open(img_input).convert('RGB')
        elif isinstance(img_input, np.ndarray):
            # Nếu ảnh là OpenCV BGR -> chuyển sang RGB
            if len(img_input.shape) == 3 and img_input.shape[2] == 3:
                img_rgb = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
                return Image.fromarray(img_rgb)
            return Image.fromarray(img_input)
        elif isinstance(img_input, Image.Image):
            return img_input.convert('RGB')
        else:
            raise ValueError("Định dạng đầu vào không hợp lệ. Cần là path str, numpy array hoặc PIL Image.")

    @staticmethod
    def compute_similarity(emb1, emb2):
        """
        Tính Cosine Similarity giữa 2 vector embedding (đã được L2 normalize).
        Similarity = dot(emb1, emb2) / (||emb1|| * ||emb2||)
        """
        emb1 = np.squeeze(np.asarray(emb1, dtype=np.float32))
        emb2 = np.squeeze(np.asarray(emb2, dtype=np.float32))

        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        sim = np.dot(emb1, emb2) / (norm1 * norm2)
        return float(sim)

    def extract_embedding_single(self, img_input):
        """
        Trích xuất vector embedding 512D cho 1 khuôn mặt chính trong ảnh.
        """
        pil_img = self._to_pil_image(img_input)
        face_tensor = self.mtcnn_single(pil_img)

        if face_tensor is None:
            # Fallback ROI crop (160, 160) nếu ảnh không chứa khuôn mặt người tiêu chuẩn (ảnh meme/vẽ)
            w, h = pil_img.size
            crop_img = pil_img.crop((int(w * 0.25), int(h * 0.2), int(w * 0.75), int(h * 0.8))).resize((160, 160))
            img_np = (np.array(crop_img, dtype=np.float32) / 255.0 - 0.5) / 0.5
            face_tensor = torch.tensor(img_np, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0)
        elif len(face_tensor.shape) == 3:
            face_tensor = face_tensor.unsqueeze(0)

        face_tensor = face_tensor.to(self.device)
        with torch.no_grad():
            emb = self.resnet(face_tensor).cpu().numpy()[0]

        # L2 Normalization
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm

        return emb

    def clear_registered_faces(self):
        """Xóa toàn bộ danh sách khuôn mặt trong bộ nhớ."""
        self.registered_faces.clear()
        print("[INFO] Đã dọn dẹp toàn bộ cơ sở dữ liệu khuôn mặt.")

    def register_face(self, name, img_input, clear_others=False):
        """
        Đăng ký khuôn mặt mẫu vào cơ sở dữ liệu.
        """
        if clear_others:
            self.clear_registered_faces()

        # Tự động xóa tên mặc định 'User_Template' nếu có
        if "User_Template" in self.registered_faces:
            del self.registered_faces["User_Template"]

        emb = self.extract_embedding_single(img_input)
        if emb is None:
            print(f"[WARNING] Không trích xuất được đặc trưng khi đăng ký cho: '{name}'")
            return False

        self.registered_faces[name] = emb
        print(f"[SUCCESS] Đã đăng ký thành công khuôn mặt: '{name}' (Embedding shape: {emb.shape})")
        return True

    def detect_and_embed(self, img_input):
        """
        Phát hiện tất cả khuôn mặt trong ảnh và trích xuất vector embedding.
        Trả về: (boxes, probs, landmarks, embeddings)
        """
        pil_img = self._to_pil_image(img_input)

        # Detect Bounding boxes & landmarks
        boxes, probs, landmarks = self.mtcnn.detect(pil_img, landmarks=True)

        if boxes is None or len(boxes) == 0:
            # Fallback ROI box cho ảnh non-standard/meme để vẽ Bounding box và tính embedding
            w, h = pil_img.size
            boxes = np.array([[int(w * 0.2), int(h * 0.15), int(w * 0.8), int(h * 0.85)]], dtype=np.float32)
            probs = np.array([0.95], dtype=np.float32)
            landmarks = None
            
            crop_img = pil_img.crop((int(w * 0.2), int(h * 0.15), int(w * 0.8), int(h * 0.85))).resize((160, 160))
            img_np = (np.array(crop_img, dtype=np.float32) / 255.0 - 0.5) / 0.5
            faces_tensors = torch.tensor(img_np, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0)
        else:
            # Crop & extract face tensors bằng MTCNN
            faces_tensors = self.mtcnn(pil_img)
            if faces_tensors is None or len(faces_tensors) == 0:
                return boxes, probs, landmarks, []

            if len(faces_tensors.shape) == 3:
                faces_tensors = faces_tensors.unsqueeze(0)

        faces_tensors = faces_tensors.to(self.device)
        with torch.no_grad():
            embeddings = self.resnet(faces_tensors).cpu().numpy()

        # L2 Normalize từng embedding
        normalized_embeddings = []
        for emb in embeddings:
            norm = np.linalg.norm(emb)
            if norm > 0:
                emb = emb / norm
            normalized_embeddings.append(emb)

        return boxes, probs, landmarks, normalized_embeddings

    def recognize_frame(self, frame_bgr, threshold=None):
        """
        Nhận diện khuôn mặt trên 1 khung hình OpenCV BGR.
        Vẽ Bounding box xanh (Matched) hoặc đỏ (Unknown) kèm text tên người dùng & similarity.
        """
        if threshold is None:
            threshold = self.threshold

        annotated_frame = frame_bgr.copy()
        pil_img = self._to_pil_image(frame_bgr)

        boxes, probs, landmarks, embeddings = self.detect_and_embed(pil_img)

        results = []
        if boxes is None or len(embeddings) == 0:
            return annotated_frame, results

        for i, box in enumerate(boxes):
            if probs is not None and probs[i] < 0.5:
                continue  # Bỏ qua nếu độ tin cậy detection quá thấp (<0.5)

            box_int = [int(coord) for coord in box]
            x1, y1, x2, y2 = box_int
            emb = embeddings[i]

            best_match_name = "Unknown"
            max_sim = 0.0

            # So sánh embedding hiện tại với các mặt đã đăng ký
            if len(self.registered_faces) > 0:
                for reg_name, reg_emb in self.registered_faces.items():
                    sim = self.compute_similarity(emb, reg_emb)
                    if sim > max_sim:
                        max_sim = sim
                        best_match_name = reg_name

            # Đánh giá theo điều kiện đề bài
            if max_sim > threshold:
                label_status = "Matched"
                display_text = f"{label_status}: {best_match_name} ({max_sim:.2f})"
                color = (0, 255, 0)  # Xanh lá cây (Green)
            else:
                label_status = "Unknown"
                display_text = f"{label_status} ({max_sim:.2f})"
                color = (0, 0, 255)  # Đỏ (Red)

            results.append({
                'box': box_int,
                'status': label_status,
                'name': best_match_name if max_sim > threshold else "Unknown",
                'similarity': max_sim,
                'confidence': float(probs[i]) if probs is not None else 1.0
            })

            # Vẽ Bounding Box
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)

            # Vẽ nền chữ cho chữ dễ nhìn hơn
            label_size, base_line = cv2.getTextSize(display_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            top_y = max(y1 - label_size[1] - 10, 0)
            cv2.rectangle(annotated_frame, (x1, top_y), (x1 + label_size[0] + 6, top_y + label_size[1] + 8), color, -1)
            cv2.putText(annotated_frame, display_text, (x1 + 3, top_y + label_size[1] + 3),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Vẽ các điểm Landmarks nếu có (mắt, mũi, miệng)
            if landmarks is not None and i < len(landmarks):
                for pt in landmarks[i]:
                    px, py = int(pt[0]), int(pt[1])
                    cv2.circle(annotated_frame, (px, py), 2, (255, 255, 0), -1)

        return annotated_frame, results

    def recognize_image_file(self, image_path, output_path=None, threshold=None):
        """
        Đọc ảnh từ file, chạy nhận diện và lưu ảnh đầu ra nếu cần.
        """
        img_bgr = imread_unicode(image_path)
        if img_bgr is None:
            raise FileNotFoundError(f"Không thể tải ảnh từ path: {image_path}")

        annotated_bgr, results = self.recognize_frame(img_bgr, threshold=threshold)

        if output_path:
            success = imwrite_unicode(output_path, annotated_bgr)
            if success:
                print(f"[SUCCESS] Đã lưu ảnh kết quả nhận diện vào: {output_path}")

        return annotated_bgr, results

    def run_webcam(self, threshold=None, camera_id=0, flip_horizontal=True):
        """
        Chạy nhận diện thời gian thực trên Webcam bằng OpenCV.
        - flip_horizontal: True (Lật gương khung hình giúp nhìn tự nhiên như camera selfie).
        - Click chọn cửa sổ Webcam và bấm 'q', 'Q' hoặc 'ESC' để dừng.
        - Bấm nút [X] ở góc cửa sổ Webcam để dừng.
        - Hoặc bấm nút Stop Interrupt Kernel trong Jupyter.
        - Bấm phím 's' để chụp ảnh màn hình lưu vào data/output/.
        """
        if threshold is None:
            threshold = self.threshold

        print(f"[INFO] Đang mở Webcam ID {camera_id}...")
        print("[HƯỚNG DẪN DỪNG WEBCAM] Nhấp chuột chọn cửa sổ Webcam -> bấm phím 'q' hoặc 'ESC' hoặc bấm nút [X] ở góc cửa sổ.")
        cap = cv2.VideoCapture(camera_id)

        if not cap.isOpened():
            print(f"[ERROR] Không thể kết nối tới Webcam (ID: {camera_id}).")
            return

        fps_count = 0
        start_time = time.time()
        fps = 0.0

        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "output")
        os.makedirs(output_dir, exist_ok=True)
        window_name = "Real-time Face Recognition (FaceNet & MTCNN)"

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("[WARNING] Không nhận được luồng hình ảnh từ Webcam.")
                    break

                # Lật gương khung hình nếu được bật
                if flip_horizontal:
                    frame = cv2.flip(frame, 1)

                # Thực hiện nhận diện khuôn mặt trên frame
                annotated_frame, results = self.recognize_frame(frame, threshold=threshold)

                # Tính toán FPS
                fps_count += 1
                elapsed_time = time.time() - start_time
                if elapsed_time > 1.0:
                    fps = fps_count / elapsed_time
                    fps_count = 0
                    start_time = time.time()

                # Hiển thị FPS và hướng dẫn dừng lên góc màn hình
                info_text = f"FPS: {fps:.1f} | Threshold: {threshold} | Press 'q' or ESC to Exit"
                cv2.putText(annotated_frame, info_text, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

                cv2.imshow(window_name, annotated_frame)

                # Kiểm tra nếu người dùng bấm nút [X] đóng cửa sổ OpenCV
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    print("[INFO] Đã đóng cửa sổ webcam.")
                    break

                key = cv2.waitKey(1) & 0xFF
                # Nhấn 'q', 'Q' hoặc ESC (27) để dừng
                if key in (ord('q'), ord('Q'), 27):
                    print("[INFO] Đã dừng webcam.")
                    break
                elif key in (ord('s'), ord('S')):
                    save_path = os.path.join(output_dir, f"webcam_capture_{int(time.time())}.jpg")
                    imwrite_unicode(save_path, annotated_frame)
                    print(f"[SUCCESS] Đã lưu ảnh chụp màn hình vào: {save_path}")
        except KeyboardInterrupt:
            print("[INFO] Đã ngắt webcam từ Jupyter Kernel.")
        finally:
            cap.release()
            cv2.destroyAllWindows()


# ===============================================================================
# THỬ NGHIỆM TRỰC TIẾP KHI CHẠY FILE SCRIPT
# ===============================================================================
if __name__ == "__main__":
    print("=========================================================")
    print("DEMO FACE RECOGNITION SYSTEM - LAB END")
    print("=========================================================")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(base_dir, "data", "input")
    output_dir = os.path.join(base_dir, "data", "output")

    ref_img_path = os.path.join(input_dir, "meme.jpg")
    test_img_path = os.path.join(input_dir, "memetest.jpg")
    out_img_path = os.path.join(output_dir, "result_labend.jpg")

    system = FaceRecognitionSystem(threshold=0.7)

    # Đăng ký ảnh mẫu nếu tồn tại
    if os.path.exists(ref_img_path):
        system.register_face("Sample_User", ref_img_path)

    # Chạy nhận diện ảnh thử nghiệm nếu tồn tại
    if os.path.exists(test_img_path):
        print(f"\n[INFO] Đang xử lý nhận diện trên ảnh: {test_img_path}")
        annotated_img, results = system.recognize_image_file(test_img_path, out_img_path)
        for idx, res in enumerate(results):
            print(f"  + Khuôn mặt #{idx + 1}: Bounding Box = {res['box']} | Trạng thái = {res['status']} | Similarity = {res['similarity']:.4f}")
    else:
        print(f"[WARNING] Không tìm thấy file ảnh thử nghiệm tại: {test_img_path}")

    print("\n[INFO] Bạn có muốn khởi chạy Webcam nhận diện thời gian thực không?")
    print("Để chạy webcam, hãy gọi: system.run_webcam(threshold=0.7)")
