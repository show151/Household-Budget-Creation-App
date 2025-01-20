家計簿ツール
この家計簿ツールは、PythonのTkinterライブラリを使用して作成されたデスクトップアプリケーションです。ユーザーは収入や支出の記録を追加し、月別のレポートを表示することができます。データはSQLiteデータベースに保存され、アプリケーションを再起動してもデータが保持されます。

特徴
収入と支出の記録: 収入や支出の金額、説明、カテゴリ、日付を簡単に入力できます。
月別レポート: 指定した月の収入と支出の合計を表示し、収支のバランスを確認できます。
直感的なGUI: Tkinterを使用した使いやすいインターフェース。
データの永続化: SQLiteデータベースを使用してデータを保存。

使い方
アプリケーションを起動すると、メインウィンドウが表示されます。
「収入の追加」ボタンをクリックして、収入の金額、説明、カテゴリ、日付を入力します。
「支出の追加」ボタンをクリックして、支出の金額、説明、カテゴリ、日付を入力します。
「月別レポートを表示」ボタンをクリックして、表示したい月と年を入力すると、その月の収入と支出のレポートが表示されます。
「終了」ボタンをクリックしてアプリケーションを終了します。

インストール
Pythonをインストールします（バージョン3.6以上推奨）。
必要なライブラリをインストールします。
pip install tkinter sqlite3
household_budget.pyファイルをダウンロードして実行します。
python household_budget.py

工夫した点
データベースの使用: SQLiteを使用してデータを永続化し、アプリケーションを再起動してもデータが失われないようにしています。
ユーザーインターフェース: Tkinterを使用して直感的なGUIを提供し、ユーザーが簡単に操作できるようにしています。
カテゴリ選択: 収入や支出のカテゴリを選択するためのドロップダウンメニューを提供し、入力の手間を減らしています。
日付の検証: 日付入力時に正しい形式（YYYY-MM-DD）であるかを検証し、誤った形式の入力を防いでいます。
レポート機能: 月別の収入と支出の合計を計算し、レポートとして表示する機能を追加しています。これにより、ユーザーは自分の収支を一目で把握できます。
