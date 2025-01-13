import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
from mysql.connector import Error

class HouseholdAccountBook:
  def __init__(self, db_config):
    self.db_config = db_config

  def add_record(self, record_type, amount, description, category):
    try:
      connection = mysql.connector.connect(**self.db_config)

      cursor = connection.cursor()
      query = "INSERT INTO records (type, amount, description, category) VALUES (%s, %s, %s, %s)"
      cursor.execute(query, (record_type, amount, description, category))
      connection.commit()
      cursor.close()
      connection.close()

    except Error as e:
      print(f"Error: {e}")

  def get_report(self):
    report = {'income': [], 'expense': [], 'total_income': 0, 'total_expense': 0}
    try:
      connection = mysql.connector.connect(**self.db_config)
      cursor = connection.cursor(dictionary=True)
      cursor.execute("SELECT * FROM records")
      records = cursor.fetchall()

      for record in records:
        if record['type'] == 'income':
          report['income'].append(record)
          report['total_income'] += record['amount']
        else:
          report['expense'].append(record)
          report['total_expense'] += record['amount']

      cursor.close()
      connection.close()

    except Error as e:
      print(f"Error: {e}")

    return report

class App:
  def __init__(self, root, db_config):
    self.root = root
    self.root.title("家計簿ツール")
    self.account_book = HouseholdAccountBook(db_config)

    self.income_button = tk.Button(root, text="収入を追加", command=self.add_income)
    self.income_button.pack(pady=10)

    self.expense_button = tk.Button(root, text="支出を追加", command=self.add_expense)
    self.expense_button.pack(pady=10)

    self.report_button = tk.Button(root, text="レポートを見る", command=self.show_report)
    self.report_button.pack(pady=10)

    self.quit_button = tk.Button(root, text="終了", command=root.quit)
    self.quit_button.pack(pady=10)

  def add_income(self):
    amount = simpledialog.askfloat("収入の金額", "収入の金額を入力してください:")
    if amount is not None:
      description = simpledialog.askstring("収入の説明", "収入の説明を入力してください:")
      if description:
        category = simpledialog.askstring("収入カテゴリ", "収入のカテゴリを入力してください:")
        if category:
          self.account_book.add_record('income', amount, description, category)
          messagebox.showinfo("成功", "収入が追加されました。")

  def add_expense(self):
    amount = simpledialog.askfloat("支出の金額", "支出の金額を入力してください:")
    if amount is not None:
      description = simpledialog.askstring("支出の説明", "支出の説明を入力してください:")
      if description:
        category = simpledialog.askstring("支出カテゴリ", "支出のカテゴリを入力してください:")
        if category:
          self.account_book.add_record('expense', amount, description, category)
          messagebox.showinfo("成功", "支出が追加されました。")

  def show_report(self):
    report = self.account_book.get_report()
    report_text = "=== 家計簿レポート ===\n\n"
    report_text += "収入:\n"
    for income in report['income']:
      report_text += f"- {income['description']} (カテゴリ: {income['category']}): ¥{income['amount']}\n"

    report_text += "\n支出:\n"
    for expense in report['expense']:
      report_text += f"- {expense['description']} (カテゴリ: {expense['category']}): ¥{expense['amount']}\n"

    report_text += f"\n合計収入: ¥{report['total_income']}\n"
    report_text += f"合計支出: ¥{report['total_expense']}\n"
    report_text += f"残高: ¥{report['total_income'] - report['total_expense']}\n"

    messagebox.showinfo("家計簿レポート", report_text)

if __name__ == "__main__":
    root = tk.Tk()

    # データベース設定
    db_config = {
        'host': 'localhost',        # データベースサーバーのホスト名
        'user': 'show515',     # データベースのユーザー名
        'password': 'HumiVeRa', # ユーザーのパスワード
        'database': 'household_account_book' # 作成したデータベース名
    }

    app = App(root, db_config)
    root.mainloop()