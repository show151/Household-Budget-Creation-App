import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import datetime
from datetime import datetime
import os

class HouseholdAccountBook:
  def __init__(self, db_name):
    self.db_name = db_name

    # テーブルを作成する
    self.create_table()

  def create_table(self):
    try:
      connection = sqlite3.connect(self.db_name)
      cursor = connection.cursor()
      cursor.execute('''
      CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        category TEXT,
        date TEXT NOT NULL
      )
      ''')
      connection.commit()
      cursor.close()
      connection.close()
    except sqlite3.Error as e:
      print(f"Error creating table: {e}")

  def add_record(self, record_type, amount, description, category, date):
    try:
      connection = sqlite3.connect(self.db_name)
      cursor = connection.cursor()
      query = "INSERT INTO records (type, amount, description, category, date) VALUES (?, ?, ?, ?, ?)"
      cursor.execute(query, (record_type, amount, description, category, date))
      connection.commit()
      cursor.close()
      connection.close()
    except sqlite3.Error as e:
      print(f"Error: {e}")

  def get_report(self):
    report = {'records': [], 'total_income': 0, 'total_expense': 0}
    try:
      connection = sqlite3.connect(self.db_name)
      cursor = connection.cursor()
      cursor.execute("SELECT * FROM records")
      records = cursor.fetchall()

      for record in records:
        # レコードの長さを確認し、適切なデータを追加
        if len(record) == 6:
          report['records'].append({
            'type': record[1],
            'amount': record[2],
            'description': record[3],
            'category': record[4],
            'date': record[5]  # 日付を追加
          })
          if record[1] == '収入':
            report['total_income'] += record[2]
          else:
            report['total_expense'] += record[2]
        else:
          print(f"Unexpected record format: {record}")

      cursor.close()
      connection.close()
    except sqlite3.Error as e:
      print(f"Error: {e}")

    return report

class App:
  def __init__(self, root, db_name):
    self.root = root
    self.root.title("家計簿ツール")
    self.account_book = HouseholdAccountBook(db_name)

    button_frame = tk.Frame(self.root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="収入の追加", command=self.add_income).pack(side=tk.LEFT)
    tk.Button(button_frame, text="支出の追加", command=self.add_expense).pack(side=tk.LEFT)
    tk.Button(button_frame, text="レポートを表示", command=self.show_report).pack(side=tk.LEFT)
    tk.Button(button_frame, text="終了", command=self.quit).pack(side=tk.LEFT)

  def add_income(self):
    amount = simpledialog.askfloat("収入の金額", "収入の金額を入力してください:")
    if amount is not None:
      description = simpledialog.askstring("収入の説明", "収入の説明を入力してください:")
      if description:
        category = simpledialog.askstring("収入カテゴリ", "収入のカテゴリを入力してください:")
        if category:
          date = simpledialog.askstring("日付", "日付を入力してください (YYYY-MM-DD):", initialvalue=datetime.now().strftime("%Y-%m-%d"))
          if date:
            self.account_book.add_record('収入', amount, description, category, date)
            messagebox.showinfo("成功", "収入が追加されました。")

  def add_expense(self):
    amount = simpledialog.askfloat("支出の金額", "支出の金額を入力してください:")
    if amount is not None:
      description = simpledialog.askstring("支出の説明", "支出の説明を入力してください:")
      if description:
        category = simpledialog.askstring("支出カテゴリ", "支出のカテゴリを入力してください:")
        if category:
          date = simpledialog.askstring("日付", "日付を入力してください (YYYY-MM-DD):", initialvalue=datetime.now().strftime("%Y-%m-%d"))
          if date:
            self.account_book.add_record('支出', amount, description, category, date)
            messagebox.showinfo("成功", "支出が追加されました。")

  def show_report(self):
    report_window = tk.Toplevel(self.root)  # 新しいウィンドウを作成
    report_window.title("家計簿レポート")

    # Treeviewの作成
    tree = ttk.Treeview(report_window, columns=("type", "amount", "description", "category", "date", "balance"), show='headings')
    tree.heading("type", text="タイプ")
    tree.heading("amount", text="金額")
    tree.heading("description", text="説明")
    tree.heading("category", text="カテゴリ")
    tree.heading("date", text="日付")
    tree.heading("balance", text="残高")

    # 各カラムの幅を設定
    tree.column("type", width=80)
    tree.column("amount", width=80)
    tree.column("description", width=200)
    tree.column("category", width=80)
    tree.column("date", width=100)
    tree.column("balance", width=80)

    # データ取得
    report = self.account_book.get_report()
        
    current_balance = 0  # 残高を保持する変数
    for record in report['records']:
      current_balance += record['amount'] if record['type'] == '収入' else -record['amount']
      tree.insert("", "end", values=(record['type'], record['amount'], record['description'], record['category'], record['date'], current_balance))


    tree.pack(expand=True, fill='both')

    # 合計金額を表示
    total_frame = tk.Frame(report_window)
    total_frame.pack(pady=10)
    total_income_label = tk.Label(total_frame, text=f"合計収入: ¥{report['total_income']}")
    total_income_label.pack()

    total_expense_label = tk.Label(total_frame, text=f"合計支出: ¥{report['total_expense']}")
    total_expense_label.pack()

    balance_label = tk.Label(total_frame, text=f"最終残高: ¥{report['total_income'] - report['total_expense']}")
    balance_label.pack()

  def quit(self):
    self.root.quit()

if __name__ == "__main__":
  root = tk.Tk()

  # データベースファイル名
  db_name = 'household_budget.db'

  # データベースファイルが存在する場合は削除
  if os.path.exists(db_name):
    os.remove(db_name)

  app = App(root, db_name)
  root.mainloop()