from frontend import PhonebookApp

def main():
    db_file = "./mycontact.db"
    app = PhonebookApp(db_file)
    app.run()

if __name__ == '__main__':
    main()

# برای ساخت فایل exe کدهای زیر را در خط فرمان ترمینال دایرکتوری پروژه اجرا کنید
# pip install  auto-py-to-exe
# auto-py-to-exe
