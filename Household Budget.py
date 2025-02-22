import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from datetime import datetime

class HouseholdAccountBook:
  def __init__(self, db_name):
    self.db_name = db_name
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
    except sqlite3.Error as e:
      print(f"Error creating table: {e}")
    finally:
      cursor.close()
      connection.close()

  def add_record(self, record_type, amount, description, category, date):
    try:
      connection = sqlite3.connect(self.db_name)
      cursor = connection.cursor()
      query = "INSERT INTO records (type, amount, description, category, date) VALUES (?, ?, ?, ?, ?)"
      cursor.execute(query, (record_type, amount, description, category, date))
      connection.commit()
    except sqlite3.Error as e:
      print(f"Error: {e}")
    finally:
      cursor.close()
      connection.close()

  def update_record(self, record_type, amount, description, category, date):
    try:
      connection = sqlite3.connect(self.db_name)
      cursor = connection.cursor()
      query = "UPDATE records SET type = ?, amount = ?, description = ?, category = ?, date = ? WHERE id = ?"
      cursor.execute(query, (record_type, amount, description, category, date, record_id))
      connection.commit()
    except sqlite3.Error as e:
      print(f"Error: {e}")
    finally:
      cursor.close()
      connection.close()

  def delete_record(self, record_id):
    try:
      connection = sqlite3.connect(self.db_name)
      cursor = connection.cursor()
      query = "DELETE FROM records WHERE id = ?"
      cursor.execute(query, (record_id,))
      connection.commit()
    except sqlite3.Error as e:
      print(f"Error: {e}")
    finally:
      cursor.close()
      connection.close()


  def get_report(self, month=None, year=None):
    report = {'records': [], 'total_income': 0, 'total_expense': 0}
    try:
      connection = sqlite3.connect(self.db_name)
      cursor = connection.cursor()

      if month and year:
        cursor.execute(
            "SELECT * FROM records WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (month, year))
      else:
        cursor.execute("SELECT * FROM records")

      records = cursor.fetchall()

      for record in records:
        if len(record) == 6:
          report['records'].append({
              'id': record[0],
              'type': record[1],
              'amount': record[2],
              'description': record[3],
              'category': record[4],
              'date': record[5]
          })
          if record[1] == '収入':
            report['total_income'] += record[2]
          else:
            report['total_expense'] += record[2]
    except sqlite3.Error as e:
      print(f"Error: {e}")
    finally:
      cursor.close()
      connection.close()

    return report

class App:
  def __init__(self, root, db_name):
    self.root = root
    self.root.title("家計簿ツール")
    self.account_book = HouseholdAccountBook(db_name)

    button_frame = tk.Frame(self.root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="収入の追加",
              command=self.add_income).pack(side=tk.LEFT)
    tk.Button(button_frame, text="支出の追加",
              command=self.add_expense).pack(side=tk.LEFT)
    tk.Button(button_frame, text="月別レポートを表示",
              command=self.show_month_report).pack(side=tk.LEFT)
    tk.Button(button_frame, text="終了", command=self.quit).pack(side=tk.LEFT)

    self.categories = ["食費", "給与", "お小遣い", "買い物", "交通費", "光熱費", "娯楽", "その他"]  # サンプルカテゴリ

    self.tree_frame = tk.Frame(self.root)
    self.tree_frame.pack(expand=True, fill="both")

    #テーブル表示
    self.show_all_records()

  def add_income(self):
    self.add_record("収入")

  def add_expense(self):
    self.add_record("支出")

  def add_record(self, record_type):
    amount = simpledialog.askfloat(
        f"{record_type}の金額", f"{record_type}の金額を入力してください:")
    if amount is not None and amount > 0:
      description = simpledialog.askstring(
          f"{record_type}の説明", f"{record_type}の説明を入力してください:")
      if description is not None:
        category = self.select_category(record_type)
        if category is not None:
          date_str = simpledialog.askstring(
              "日付", "日付を入力してください (YYYY/MM/DD):", initialvalue=datetime.now().strftime("%Y-%m-%d"))
          if date_str is not None:
            if self.validate_date(date_str):
              self.account_book.add_record(
                  record_type, amount, description, category, date_str)
              self.show_all_records()
              messagebox.showinfo("成功", f"{record_type}が追加されました。")
            else:
              messagebox.showerror(
                  "エラー", "日付の形式が正しくありません。YYYY-MM-DD形式で入力してください。")
          else:
            messagebox.showinfo("キャンセル", "入力がキャンセルされました。")
        else:
          messagebox.showinfo("キャンセル", "入力がキャンセルされました。")
      else:
        messagebox.showinfo("キャンセル", "入力がキャンセルされました。")
    elif amount is None:
      messagebox.showinfo("キャンセル", "入力がキャンセルされました。")
    else:
      messagebox.showerror("エラー", f"{record_type}の金額は正の数である必要があります。")

  def select_category(self, record_type):
      """ カテゴリを選択するためのダイアログを表示 """
      category_window = tk.Toplevel(self.root)
      category_window.title(f"{record_type}カテゴリを選択")

      tk.Label(category_window, text=f"{record_type}のカテゴリを選択してください:").pack(pady=10)

      selected_category = tk.StringVar(value=self.categories[0])

      dropdown = ttk.Combobox(category_window, textvariable=selected_category)
      dropdown['values'] = self.categories
      dropdown.pack(pady=10)

      def on_select():
        category_window.destroy()

      tk.Button(category_window, text="OK", command=on_select).pack(pady=10)

      self.root.wait_window(category_window)

      return selected_category.get()

  def validate_date(self, date_str):
    """ 日付が正しい形式（YYYY/MM/DD）であるか検証 """
    try:
      datetime.strptime(date_str, "%Y-%m-%d")
      return True
    except ValueError:
      return False

  def show_month_report(self):
    """ ユーザーが指定した月のレポートを表示 """
    month = simpledialog.askinteger(
      "月を入力", "月を入力してください (1-12):", minvalue=1, maxvalue=12)
    if month is not None:
      year = simpledialog.askinteger(
        "年を入力", "年を入力してください (例: 2023):", minvalue=2000, maxvalue=2100)
      if year is not None:
        report = self.account_book.get_report(f"{month:02}", str(year))
        self.display_month_report(report, month, year)
      else:
        messagebox.showinfo("キャンセル", "入力がキャンセルされました。")
    else:
      messagebox.showinfo("キャンセル", "入力がキャンセルされました。")

  def display_month_report(self, report, month, year):
    """ レポートを表示するためのウィンドウを作成 """

    report_window = tk.Toplevel(self.root)
    report_window.title(f"{year}年{month}月のレポート")

    tree = ttk.Treeview(report_window, columns=(
      "type", "amount", "description", "category", "date"), show='headings')

    tree.heading("type", text="タイプ")
    tree.heading("amount", text="金額")
    tree.heading("description", text="説明")
    tree.heading("category", text="カテゴリ")
    tree.heading("date", text="日付")

    for record in report['records']:
      tree.insert("", "end", values=(
        record['type'], record['amount'], record['description'], record['category'], record['date']))

    tree.pack(expand=True, fill='both')

    total_frame = tk.Frame(report_window)
    total_frame.pack(pady=10)
    total_income_label = tk.Label(
      total_frame, text=f"合計収入: ¥{report['total_income']}")
    total_income_label.pack()

    total_expense_label = tk.Label(
      total_frame, text=f"合計支出: ¥{report['total_expense']}")
    total_expense_label.pack()

    balance_label = tk.Label(
      total_frame, text=f"最終残高: ¥{report['total_income'] - report['total_expense']}")
    balance_label.pack()

  def display_report(self, report):
    """ レポートを表示するためのtreeを作成 """
    for widget in self.tree_frame.winfo_children():
            widget.destroy()

    tree = ttk.Treeview(self.tree_frame, columns=(
      "type", "amount", "description", "category", "date"), show='headings')
        
    tree.heading("type", text="タイプ")
    tree.heading("amount", text="金額")
    tree.heading("description", text="説明")
    tree.heading("category", text="カテゴリ")
    tree.heading("date", text="日付")

    for record in report['records']:
      tree.insert("", "end", values=(
        record['type'], record['amount'], record['description'], record['category'], record['date']))

    tree.pack(expand=True, fill='both')

    button_frame = tk.Frame(self.tree_frame)
    button_frame.pack(pady=10)

    edit_button = tk.Button(button_frame, text="編集", command=lambda:self.edit_record(tree))
    edit_button.pack(side=tk.LEFT, padx=5)

    delete_button = tk.Button(button_frame, text="削除", command=lambda: self.delete_record(tree))
    delete_button.pack(side=tk.LEFT, padx=5)

    total_frame = tk.Frame(self.tree_frame)
    total_frame.pack(pady=10)
    total_income_label = tk.Label(
      total_frame, text=f"合計収入: ¥{report['total_income']}")
    total_income_label.pack()

    total_expense_label = tk.Label(
      total_frame, text=f"合計支出: ¥{report['total_expense']}")
    total_expense_label.pack()

    balance_label = tk.Label(
      total_frame, text=f"最終残高: ¥{report['total_income'] - report['total_expense']}")
    balance_label.pack()

  def show_all_records(self):
    report = self.account_book.get_report()
    self.display_report(report)

  def quit(self):
    self.root.quit()

if __name__ == "__main__":
  root = tk.Tk()

  # データベースファイル名
  db_name = 'household_budget.db'

  # データベースファイルが存在する場合は削除
  #if os.path.exists(db_name):
    #os.remove(db_name)

  app = App(root, db_name)
  root.mainloop()
