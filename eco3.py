import tkinter as tk
import requests
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

# Lưu đường dẫn ảnh chân dung đã xoá nền
image_path = ""

# Hàm gọi API Remove.bg để xoá nền ảnh
def remove_background(image_path):
    api_key = 'aT27DhgMkcEWQkkNbVabUqeK'

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        headers={'X-Api-Key': api_key},
        files={'image_file': open(image_path, 'rb')}
    )

    if response.status_code == requests.codes.ok:
        with open('no_bg.png', 'wb') as out:
            out.write(response.content)
        return 'no_bg.png'
    else:
        return None

# Hàm xử lý khi người dùng nhấn nút "Chọn ảnh"
def select_image():
    global image_path
    image_path = filedialog.askopenfilename()
    entry_path.delete(0, tk.END)
    entry_path.insert(tk.END, image_path)

# Hàm xử lý khi người dùng nhấn nút "Upload"
def upload_image():
    global img_portrait, img_background_copy
    
    # Lấy đường dẫn file ảnh
    image_path = entry_path.get()

    if image_path:
        try:
            # Xoá nền ảnh sử dụng API Remove.bg
            removed_bg_image = remove_background(image_path)

            if removed_bg_image:
                # Resize ảnh đã xoá nền về kích thước 450x650
                img_portrait = Image.open(removed_bg_image).convert("RGBA")
                img_portrait_resized = img_portrait.resize((450, 650))

                # Tính toán vị trí để ghép ảnh vào nền
                x = img_background_copy.width - img_portrait_resized.width
                y = img_background_copy.height - img_portrait_resized.height

                # Lấy đối xứng của x nếu x < 0
                if x < 0:
                    x = 0

                # Ghép ảnh đã xoá nền vào vị trí sát cạnh dưới cùng của ảnh nền
                img_background_copy.paste(img_portrait_resized, (x, y), mask=img_portrait_resized)

                # Hiển thị ảnh ghép
                photo_merged = ImageTk.PhotoImage(img_background_copy)
                label_background_image.configure(image=photo_merged)
                label_background_image.image = photo_merged
        
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    else:
        messagebox.showerror("Lỗi", "Bạn chưa chọn ảnh!")

if __name__ == "__main__":
    # Tạo cửa sổ
    window = tk.Tk()
    window.title("Blend ảnh đã xoá nền")

    # Khởi tạo img_background_copy
    bg = Image.open("C:\\Users\\ADMIN\\Desktop\\Eco\\1.jpg")
    img_background_copy = bg.copy()

    # Tạo nút "Chọn ảnh"
    btn_select = tk.Button(window, text="Chọn ảnh", command=select_image)
    btn_select.pack()

    # Hiển thị đường dẫn file được chọn
    entry_path = tk.Entry(window)
    entry_path.pack()

    # Tạo nút "Upload"
    btn_upload = tk.Button(window, text="Upload", command=upload_image)
    btn_upload.pack()

    # Hiển thị hình nền cố định
    photo_background = ImageTk.PhotoImage(bg)
    label_background_image = tk.Label(window, image=photo_background)
    label_background_image.pack()

    # Bắt đầu chạy ứng dụng
    window.mainloop()