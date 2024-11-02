# -*- coding: utf-8 -*-
import os
import sys
import configparser
import re
import json
import random
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox, Menu
from glob import glob
from settings_window import settings, cleanup_ini_file
from check_settings import validate_settings, sanitize_input


version = "1.0.28"


# 言語設定の読み込み
config = configparser.ConfigParser()
settings_path = os.path.join(os.path.dirname(sys.argv[0]), 'settings.ini')
if not os.path.exists(settings_path):  # iniファイルがない場合はデフォルト値で新規作成
    config['Settings'] = {
        'lang': 'en', 
        'increment_unit': '0.05',  # 0.1単位か0.05単位のみ許可
        'window_width': '1000',  # 初期ウィンドウ幅
        'window_height': '600',   # 初期ウィンドウ高さ
        'itemarea_displines': '5',  # アイテム欄の表示行数(高さ)
        'scroll_lines': '3',  # マウスホイールによる単位スクロール行数
        'messages': 'enable',  # メッセージの表示(enable)と抑止(disable)
        'autosave_json': 'disable',  # JSON辞書ファイルの自動保存設定
        'backup_json': 'enable',  # アプリ起動時にJSON辞書ファイルを自動バックアップする設定
        'textfont': 'TkDefaultFont',  # TkDefaultFontはTkinterのデフォルトシステムフォント
        'fontsize_treeview': '12',  # ツリー表示のフォントサイズ
        'fontsize_textbox': '12',  # テキストボックス表示のフォントサイズ
        'datetime_format': '%%Y%%m%%d_%%H%%M%%S',  # '20240826_232125'のようなフォーマット(2024年8月26日 23時21分25秒の場合)
        'multiple_boot': 'disable',
    }
    with open(settings_path, 'w') as configfile:
        config.write(configfile)

else:  # iniファイルが既にある場合は読み込むが、設定値があるかチェックし、ない場合は追加する
    # ゴミ除去(保険処理)
    cleanup_ini_file(settings_path)
    # inファイルを読む
    config.read(settings_path)

    # 'Settings'セクションが存在しない場合は新規作成
    if 'Settings' not in config:
        config['Settings'] = {}

    # 各設定項目の確認とデフォルト値の追加
    default_settings = {
        'lang': 'en',
        'increment_unit': '0.05',
        'window_width': '1000',
        'window_height': '600',
        'itemarea_displines': '5',
        'scroll_lines': '3',
        'messages': 'enable',
        'autosave_json': 'disable',
        'backup_json': 'enable',
        'textfont': 'TkDefaultFont',
        'fontsize_treeview': '12',
        'fontsize_textbox': '12',
        'datetime_format': '%%Y%%m%%d_%%H%%M%%S',
        'multiple_boot': 'disable',
    }

    for key, value in default_settings.items():
        if key not in config['Settings']:
            config['Settings'][key] = value

    # 設定をINIファイルに書き込む
    with open(settings_path, 'w') as configfile:
        config.write(configfile)


# メッセージとラベル
messages = {
    'ja': {
        'button_add_parent': '親追加',
        'button_add_child': '子追加',
        'button_expand': '+',
        'button_collapse': '-',
        'button_delete': '削除',
        'button_settings': '設定',
        'check_autosave_json': '辞書オートセーブ',
        'button_save_json': '辞書セーブ',
        
        'button_update': '更新',
        'button_list': '一覧',
        'button_load': 'ロード',
        'button_save': 'セーブ',
        'button_copy': 'コピー',
        'button_shuffle': 'シャッフル',
        'check_lock': 'ロック',
        'button_clear': 'クリア',
        'button_copy_text': 'テキストをクリップボードにコピー',
        'button_clone_item': 'このアイテムを複製する',
        'button_add_fav': 'お気に入りに追加',
        'button_close': '閉じる',
        'label_search': '検索',
        'button_apply': '適用',

        'tab_chunks': '  チャンク  ',
        'tab_words':  '    単語    ',
        'tab_favorites':  ' お気に入り ',

        'title_error': 'エラー',
        'message_multipleboot_error': 'アプリケーションは既に実行されています。',

        'title_load': 'ロード',
        'message_load': 'ファイルを読み込みました。',
        'title_save': 'セーブ',
        'message_save': 'ファイルを保存しました。',
        'title_save_error': 'セーブエラー',
        'message_text_empty': 'テキストボックスが空です。',

        'title_clone_info': 'アイテム複製',
        'message_clone_complete': 'アイテムを複製しました。',

        'title_fav_info': 'お気に入り追加',
        'message_fav_complete': ' をお気に入りに追加しました。',  # 先頭にスペース入れる

        'title_select_error': '選択エラー',
        'message_select_favitem': 'お気に入りに追加するアイテムを選択してください。',
        'message_select_item_to_add': '子アイテムを追加する場所を選択してください。',

        'title_delete_error': '削除エラー',
        'message_select_item_to_delete': '削除対象アイテムを選択してください。',
        'message_favparent_deletion_error': 'お気に入りの親アイテムは削除できません。',
        'message_parent_needs_child': '親アイテムには最低一つの子アイテムが必要です。',
        'message_parent_needs_one': '親アイテムは最低一つ残す必要があります。',

        'title_update_error': '更新エラー',
        'message_select_item': '更新対象アイテムを選択してください。',
        'message_item_exists': '他の親アイテムと内容が一致しています。同じ内容を登録することはできません。',

        'title_update_complete': '更新完了',
        'message_item_updated': 'アイテムが更新されました。',

        'title_copy_complete': 'コピー完了',
        'message_prompt_copied': '作成したプロンプトをクリップボードにコピーしました。',
        'message_item_copied': 'アイテムテキストをクリップボードにコピーしました。',

        'title_format_error': 'テキスト構文エラー',
        'messages_unbalanced_brackets': '括弧が適切に閉じられていません。',
        
        'title_clear_confirm': 'クリア確認',
        'message_prompt_cleared': '作成したプロンプトを消去します。本当によろしいですか？',

        'title_delete_confirm': '削除確認',
        'message_item_deleted': '選択したアイテムを削除します。削除していいですか？',
        'message_item_deleted_with_children': '配下のアイテムも一緒にすべて削除されます。削除していいですか？',

        'title_prompt_error': '一覧エラー',
        'message_prompt_listitem_notfound': '一覧表示できるファイルがありません。',
        'title_close': '閉じる',

        'title_save_json': '辞書セーブ',
        'message_save_json_complete': '辞書ファイルを保存しました。',
        'title_save_json_error': '辞書セーブエラー',
        'message_save_json_notcomplete': '辞書ファイルの保存に失敗しました: ',
        
        'title_exit_confirm': '終了前確認',
        'message_autosave_disabled_confirm': '\'辞書オートセーブ\'が無効になっています。アプリを終了してもいいですか？ \nアプリを終了する場合は\'OK\'を押してください。\n終了前に辞書を保存したい場合は\'キャンセル\'を押してから、\'辞書セーブ\'ボタンを押してください。'
    },
    'en': {
        'button_add_parent': 'Add Parent',
        'button_add_child': 'Add Child',
        'button_expand': '+',
        'button_collapse': '-',
        'button_delete': 'Delete',
        'button_settings': 'Settings',
        'check_autosave_json': 'Auto Save dicts.',
        'button_save_json': 'Save dicts.',
        
        'button_update': 'Update',
        'button_list': 'List',
        'button_load': 'Load',
        'button_save': 'Save',
        'button_copy': 'Copy',
        'button_shuffle': 'Shuffle',
        'check_lock': 'Lock',
        'button_clear': 'Clear',
        'button_copy_text': 'Copy text to clipboard',
        'button_clone_item': 'Clone this item',
        'button_add_fav': 'Add to favorites',
        'button_close': 'Close',
        'label_search': 'Search',
        'button_apply': 'Apply',
        
        'tab_chunks': '  Chunks  ',
        'tab_words':  '   Words   ',
        'tab_favorites':  '  Favorites  ',

        'title_error': 'Error',
        'message_multipleboot_error': 'The application is already running.',

        'title_load': 'Load',
        'message_load': 'File loaded successfully.',
        'title_save': 'Save',
        'message_save': 'File saved successfully.',
        'title_save_error': 'Save Error',
        'message_text_empty': 'Textbox is empty.',

        'title_clone_info': 'Cloning item Complete',
        'message_clone_complete': 'Item cloned successfully.',

        'title_fav_info': 'Fav Complete',
        'message_fav_complete': ' is added to Favorites.',  # 先頭にスペース入れる

        'title_select_error': 'Selection Error',
        'message_select_favitem': 'Select an item to add to Favorites.',
        'message_select_item_to_add': 'Select a place to add a child item.',

        'title_delete_error': 'Deletion Error',
        'message_select_item_to_delete': 'Please select an item to delete.',
        'message_favparent_deletion_error': 'Parent items of Fav. cannot be deleted.',
        'message_parent_needs_child': 'A parent item must have at least one child item.',
        'message_parent_needs_one': 'At least one parent item must remain.',

        'title_update_error': 'Update Error',
        'message_select_item': 'Please select an item to update.',
        'message_item_exists': 'Another parent item with the same content already exists. Cannot register the same content.',

        'title_update_complete': 'Update Completed',
        'message_item_updated': 'Item has been updated.',

        'title_copy_complete': 'Copy Complete',
        'message_prompt_copied': 'Prompt copied to clipboard.',
        'message_item_copied': 'Item text copied to clipboard.',

        'title_format_error': 'Text format Error',
        'messages_unbalanced_brackets': 'Unbalanced brackets Error.',
        
        'title_clear_confirm': 'Clear Confirmation',
        'message_prompt_cleared': 'Are you sure you want to clear the created prompt?',

        'title_delete_confirm': 'Delete Confirmation',
        'message_item_deleted': 'Are you sure you want to delete the selected item?',
        'message_item_deleted_with_children': 'All items under the selected item will also be deleted. Are you sure?',

        'title_prompt_error': 'Listing Error',
        'message_prompt_listitem_notfound': 'No files found to list.',
        'title_close': 'Close',

        'title_save_json': 'Save dicts.',
        'message_save_json_complete': 'Save dicts. Completed.',
        'title_save_json_error': 'Save dicts. Error',
        'message_save_json_notcomplete': 'Save dicts. Failed: ',
        
        'title_exit_confirm': 'Exit Confirmation',
        'message_autosave_disabled_confirm': '\'Auto save dicts.\' is disabled. Are you sure you want to exit the application? \nPress \'OK\' to Close App. \nPress \'CANCEL\' & \'Save dicts.\' if you want to save dictionary files before exit.'
    }
}

initial_data_chunks = {
    "Chunks 001": ["1","2","3"],
    "Chunks 002": ["1","2","3"],
    "Chunks 003": ["1","2","3"]
    }

initial_data_words = {
    "Words 001": ["1","2","3"],
    "Words 002": ["1","2","3"],
    "Words 003": ["1","2","3"]
    }

initial_data_favorites = {
    "Fav:Chunks": [],
    "Fav:Words": []
    }

fontsize_min = 8
fontsize_max = 32
rowheight_treeview = 1  # 後で更新

# アプリケーションの開始時にロックファイルを作成
lock_file_path = 'app.lock'


class PromptConstructorMain:
    def __init__(self):
        global rowheight_treeview

        try:
            self.load_settings()

        except Exception as e:
            messagebox.showerror("Configuration Error", str(e))
            exit(1)

        if multiple_boot == 'disable':
            if os.path.exists(lock_file_path):
                messagebox.showerror(messages[lang]['title_error'], messages[lang]['message_multipleboot_error'])
                sys.exit(1)
            else:
                open(lock_file_path, 'w').close()  # ロックファイルを作成


        root = tk.Tk()
        self.root = root
        self.root.title("Prompt Constructor v" + version)
        self.root.geometry(f"{window_width}x{window_height}")


        # # プロンプト欄のカーソル位置を記憶する
        # def on_text_box_focus_out(self, event):
        #     self.cursor_position = self.text_box_bottom.index(tk.INSERT)
        # # プロンプト欄のカーソル位置を記憶しておいた位置に戻す(再現する)
        # def on_text_box_focus_in(self, event):
        #     if self.cursor_position:
        #         self.text_box_bottom.mark_set(tk.INSERT, self.cursor_position)
        #         self.text_box_bottom.see(tk.INSERT)

        # アプリ起動時に実行
        self.ensure_prompt_files_exist()

        self.undo_history = []  # UNDO用の履歴スタック
        self.redo_history = []  # REDO用の履歴スタック

        # ボタンの幅設定(例外あり)
        self.button_width1 = 8

        # SHIFTキー押下判定用
        self.is_shift_pressed = False

        style = ttk.Style()
        style.configure("Treeview", font=(textfont, fontsize_treeview), rowheight=rowheight_treeview)  # ツリービューのスタイル設定

        # 左右ペインを分割するためのPanedWindow
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=10)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # 左ペイン (ツリービュー)
        self.left_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame, width=300)

        # ボタンフレーム (左ペインの上部に配置)
        self.button_frame = tk.Frame(self.left_frame)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # 「親追加」ボタン
        self.add_parent_button = tk.Button(self.button_frame, text=messages[lang]['button_add_parent'], width=10, command=self.on_add_parent_button_click)
        self.add_parent_button.pack(side=tk.LEFT)

        # 「子追加」ボタン
        self.add_child_button = tk.Button(self.button_frame, text=messages[lang]['button_add_child'], width=10, command=self.on_add_child_button_click)
        self.add_child_button.pack(side=tk.LEFT)

        # 「展開」ボタン
        self.expand_button = tk.Button(self.button_frame, text=messages[lang]['button_expand'], width=3, command=self.expand_all)
        self.expand_button.pack(side=tk.LEFT)

        # 「閉じる」ボタン
        self.collapse_button = tk.Button(self.button_frame, text=messages[lang]['button_collapse'], width=3, command=self.collapse_all)
        self.collapse_button.pack(side=tk.LEFT)

        # 「削除」ボタン
        self.delete_button = tk.Button(self.button_frame, text=messages[lang]['button_delete'], width=6, command=self.on_delete_button_click)
        self.delete_button.pack(side=tk.RIGHT)

        # タブコントロールの作成
        self.tab_control = ttk.Notebook(self.left_frame)
        self.tab_control.pack(fill=tk.BOTH, expand=True)

        # タブ1 (dict_chunks.json)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text=messages[lang]['tab_chunks'])

        # タブ2 (dict_words.json)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text=messages[lang]['tab_words'])

        # タブ3 (dict_favorites.json)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab3, text=messages[lang]['tab_favorites'])

        # タブ1のツリービュー
        self.tree1 = ttk.Treeview(self.tab1, style="Treeview")
        self.tree1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        # タブ1のスクロールバー
        self.tree1_scrollbar = ttk.Scrollbar(self.tab1, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=self.tree1_scrollbar.set)
        self.tree1_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # タブ2のツリービュー
        self.tree2 = ttk.Treeview(self.tab2, style="Treeview")
        self.tree2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # タブ2のスクロールバー
        self.tree2_scrollbar = ttk.Scrollbar(self.tab2, orient="vertical", command=self.tree2.yview)
        self.tree2.configure(yscrollcommand=self.tree2_scrollbar.set)
        self.tree2_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # タブ3のツリービュー
        self.tree3 = ttk.Treeview(self.tab3, style="Treeview")
        self.tree3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # タブ3のスクロールバー
        self.tree3_scrollbar = ttk.Scrollbar(self.tab3, orient="vertical", command=self.tree3.yview)
        self.tree3.configure(yscrollcommand=self.tree3_scrollbar.set)
        self.tree3_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # JSONファイルのロード
        self.load_dicts_from_json()

        # 前回選択したアイテムを記録する変数
        self.last_selected_parent = None
        self.last_selected_child = None


        # ツリービューのイベントをバインド
        for tree in [self.tree1, self.tree2, self.tree3]:
            tree.bind("<<TreeviewSelect>>", self.on_tree_select)
            tree.bind("<ButtonPress-1>", self.on_tree_item_press)
            tree.bind("<ButtonPress-3>", self.on_tree_item_press2)
            tree.bind("<B1-Motion>", self.on_tree_item_motion)
            tree.bind("<ButtonRelease-1>", self.on_tree_item_release)

        # ドラッグデータの初期化
        self.drag_data = {"x": 0, "y": 0, "item": None, "tree": None}

        # 右ペイン
        self.right_frame = ttk.PanedWindow(self.paned_window, orient=tk.VERTICAL)
        self.paned_window.add(self.right_frame, minsize=200)  # 最小サイズを設定

        # 右ペインの上部フレーム (テキストボックスと「更新」ボタン)
        self.right_frame_top = tk.Frame(self.right_frame)
        self.right_frame.add(self.right_frame_top)

        # 下部フレームに脇にボタンを縦に配置するためのフレーム
        self.button_vertical_frame2 = tk.Frame(self.right_frame_top)
        self.button_vertical_frame2.pack(side=tk.LEFT, padx=5)

        # 「更新」ボタン
        self.update_button = tk.Button(self.button_vertical_frame2, text=messages[lang]['button_update'], width=self.button_width1, command=self.on_update_button_click)
        self.update_button.pack(side=tk.TOP, pady=(5, 0))
        # 「コピー2」ボタン(ツリービューの選択アイテムのテキストをコピーする)
        self.copy2_button = tk.Button(self.button_vertical_frame2, text=messages[lang]['button_copy'], width=self.button_width1, command=self.on_copy2_button_click)
        self.copy2_button.pack(side=tk.TOP, pady=(5, 0))

        # 上部テキストボックス(アイテム欄)
        self.text_box_top = tk.Text(self.right_frame_top, height=itemarea_displines, wrap=tk.NONE)
        # 先にスクロールバーを初期化して先に配置してしまう
        self.text_box_top_scrollbar = ttk.Scrollbar(self.right_frame_top, orient="vertical", command=self.text_box_top.yview)
        self.text_box_top_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_box_top.configure(yscrollcommand=self.text_box_top_scrollbar.set)
        # スクロールバーの後、上部テキストボックスをpack
        self.text_box_top.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_box_top.config(font=(textfont, fontsize_textbox), takefocus=0)

        # 右ペインの下部フレーム (テキストボックスと「クリア」ボタン等)
        self.right_frame_bottom = tk.Frame(self.right_frame)
        self.right_frame.add(self.right_frame_bottom)

        # 下部フレームに脇にボタンを縦に配置するためのフレーム
        self.button_vertical_frame = tk.Frame(self.right_frame_bottom)
        self.button_vertical_frame.pack(side=tk.LEFT, padx=5, pady=0)

        # 「一覧」ボタンを追加
        self.list_button = tk.Button(self.button_vertical_frame, text=messages[lang]['button_list'], width=self.button_width1, command=self.on_list_button_click)
        self.list_button.pack(side=tk.TOP)

        # 「ロード」ボタンの追加
        self.load_button = tk.Button(self.button_vertical_frame, text=messages[lang]['button_load'], width=self.button_width1, command=self.on_load_button_click)
        self.load_button.pack(side=tk.TOP, pady=(5, 0))

        # 「セーブ」ボタンの追加
        self.save_button = tk.Button(self.button_vertical_frame, text=messages[lang]['button_save'], width=self.button_width1, command=self.on_save_button_click)
        self.save_button.pack(side=tk.TOP, pady=(5, 0))

        # 「コピー」ボタン(プロンプト欄のテキストをコピーする)
        self.copy_button = tk.Button(self.button_vertical_frame, text=messages[lang]['button_copy'], width=self.button_width1, command=self.on_copy_button_click)
        self.copy_button.pack(side=tk.TOP, pady=(40, 0))

        # 「シャッフル」ボタン
        self.shuffle_button = tk.Button(self.button_vertical_frame, text=messages[lang]['button_shuffle'], width=self.button_width1, command=self.on_shuffle_button_click)
        self.shuffle_button.pack(side=tk.TOP, pady=(5, 0))

        # 「ロック」チェックボックスとラベル
        self.lock_var = tk.BooleanVar(value=False)  # ロック状態を管理する変数
        self.lock_checkbox = tk.Checkbutton(self.button_vertical_frame, text=messages[lang]['check_lock'], variable=self.lock_var, command=self.toggle_lock)
        self.lock_checkbox.pack(side=tk.TOP, pady=(40, 0))  # 上方向、間隔を少し広めに取る

        # 「クリア」ボタン
        self.clear_button = tk.Button(self.button_vertical_frame, text=messages[lang]['button_clear'], width=self.button_width1, command=self.on_clear_button_click)
        self.clear_button.pack(side=tk.TOP, pady=(5, 40))

        # 下部テキストボックス(プロンプト欄)
        self.text_box_bottom = tk.Text(self.right_frame_bottom, height=10)
        # 先にスクロールバーを初期化して先に配置してしまう
        self.text_box_bottom_scrollbar = ttk.Scrollbar(self.right_frame_bottom, orient="vertical", command=self.text_box_bottom.yview)
        self.text_box_bottom_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_box_bottom.configure(yscrollcommand=self.text_box_bottom_scrollbar.set)
        # スクロールバーの後、上部テキストボックスをpack
        self.text_box_bottom.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_box_bottom.config(state=tk.NORMAL)  # テキストボックスの編集状態を初期化
        self.text_box_bottom.config(font=(textfont, fontsize_textbox), takefocus=0)  # システムフォントを使用
        self.text_box_bottom.focus()
        
        # 検索欄
        self.text_box_search = EntryWithPlaceholder(self.right_frame_bottom, placeholder=messages[lang]['label_search'], color='gray')
        self.text_box_search.pack(fill=tk.BOTH, padx=5, pady=5)
        self.text_box_search.config(state=tk.NORMAL)  # テキストボックスの編集状態を初期化
        self.text_box_search.config(font=(textfont, fontsize_textbox), takefocus=0)  # システムフォントを使用

        # イベントバインド
        # self.text_box_search.bind("<<Modified>>", self.on_entry_change)
        self.text_box_search.bind('<KeyRelease>', self.update_highlight)

        self.text_box_top.bind('<ButtonRelease-1>', self.update_highlight)  # マウスボタンが離されたときに呼び出す
        self.text_box_top.bind('<B1-Motion>', self.update_highlight)  # ドラッグ中に呼び出す
        self.text_box_top.bind('<KeyRelease>', self.update_highlight)
        self.text_box_top.bind('<<Selection>>', self.update_highlight)
        self.text_box_top.bind('<Control-a>', self.update_highlight)
        self.text_box_top.bind('<<Paste>>', self.update_highlight)  # 右クリックメニューからの選択にも対応
        self.text_box_top.bind('<<UpdateText>>', self.update_highlight)  # ファイル読み込み時
        self.text_box_top.bind('<<Modified>>', self.update_highlight)

        self.text_box_bottom.bind('<ButtonRelease-1>', self.update_highlight)  # マウスボタンが離されたときに呼び出す
        self.text_box_bottom.bind('<B1-Motion>', self.update_highlight)  # ドラッグ中に呼び出す
        self.text_box_bottom.bind('<KeyRelease>', self.update_highlight)
        self.text_box_bottom.bind('<<Selection>>', self.update_highlight)
        self.text_box_bottom.bind('<Control-a>', self.update_highlight)
        self.text_box_bottom.bind('<<Paste>>', self.update_highlight)  # 右クリックメニューからの選択にも対応
        self.text_box_bottom.bind('<<UpdateText>>', self.update_highlight)  # ファイル読み込み時
        self.text_box_bottom.bind('<<Modified>>', self.update_highlight)
        self.text_box_bottom.bind('<Key>', self.update_highlight)


        # マウスホイールイベントのバインド
        for tree in [self.tree1, self.tree2, self.tree3]:
            tree.bind("<Shift-MouseWheel>", self.on_mousewheel_leftpane)
            tree.bind("<MouseWheel>", self.scroll_leftpane)
            tree.bind("<Button-2>", self.on_mouseclick_leftpane)
        for text_box in [self.text_box_top, self.text_box_bottom, self.text_box_search]:
            text_box.bind("<Shift-MouseWheel>", self.on_mousewheel_rightpane)
            text_box.bind("<Button-2>", self.on_mouseclick_rightpane)

        # フォントサイズ変更関連変数 初期化
        self.fontsize_treeview_current = fontsize_treeview
        rowheight_treeview = self.fontsize_treeview_current + 10
        style = ttk.Style()
        style.configure("Treeview", font=(textfont, self.fontsize_treeview_current), rowheight=rowheight_treeview)
        self.fontsize_textbox_current = fontsize_textbox


        # JSON保存関連のチェックボックスとボタンを配置するフレーム
        self.json_options_frame = tk.Frame(self.left_frame)
        self.json_options_frame.pack(side=tk.BOTTOM, pady=5)

        # 設定ボタン
        self.settings_button = tk.Button(self.json_options_frame, text=messages[lang]['button_settings'], width=8, command=self.open_settings)  # コマンドは適宜設定
        self.settings_button.pack(side=tk.LEFT, padx=(0, 25))
        self.settings_window = None  # 設定ウインドウインスタンス

        # 「辞書セーブ」ボタン
        self.save_json_button = tk.Button(self.json_options_frame, text=messages[lang]['button_save_json'], width=10, command=self.save_dicts_to_json)
        self.save_json_button.pack(side=tk.RIGHT, padx=(5, 0))

        # 「辞書オートセーブ」設定のチェックボックス
        self.autosave_json_var = tk.BooleanVar(value=autosave_json_enabled)
        self.autosave_json_checkbox = tk.Checkbutton(self.json_options_frame, text=messages[lang]['check_autosave_json'], variable=self.autosave_json_var, command=self.toggle_autosave_json)
        self.autosave_json_checkbox.pack(side=tk.RIGHT,  padx=(20, 0))

        # 前回選択したアイテムを記録する変数
        self.last_selected_parent = None
        self.last_selected_child = None

        self.text_box_top.bind("<Control-Up>", self.on_ctrl_arrow_key)
        self.text_box_top.bind("<Control-Down>", self.on_ctrl_arrow_key)
        self.text_box_bottom.bind("<Control-Up>", self.on_ctrl_arrow_key)
        self.text_box_bottom.bind("<Control-Down>", self.on_ctrl_arrow_key)
        self.text_box_bottom.bind('<KeyRelease>', self.save_to_history1)

        self.root.bind("<Double-Button-1>", self.on_double_click)  # プロンプト欄では正常動作しなかったのでrootを監視(上のテキスト欄でも動作する)

        # タブ切り替え時のイベントをバインド
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # キーバインドの設定
        self.root.bind("<Control-z>", self.undo)
        self.root.bind("<Control-y>", self.redo)
        self.root.bind("<Escape>", self.on_exit)

        # Shift監視
        self.root.bind("<KeyPress-Shift_L>", self.on_shift_press)
        self.root.bind("<KeyRelease-Shift_L>", self.on_shift_release)
        self.root.bind("<KeyPress-Shift_R>", self.on_shift_press)
        self.root.bind("<KeyRelease-Shift_R>", self.on_shift_release)

        # Ctrl+F監視
        self.root.bind("<Control-f>", self.focus_search_box)

        # 過去に自動保存されたtmpファイルを読み込む(text_box_bottomが配置された後でないと動作しないので注意)
        self.load_latest_prompt_file()

        self.start()


    def load_settings(self):
        """設定値を読み込み、バリデーションとサニタイズを行う関数
        """
        config = configparser.ConfigParser()
        settings_path = os.path.join(os.path.dirname(sys.argv[0]), 'settings.ini')
        config.read(settings_path)

        settings = {}
        # for key in config['Settings']:
        #     settings[key] = config['Settings'][key]
        settings = {
            'lang': config['Settings']['lang'],
            'increment_unit': float(config['Settings']['increment_unit']),
            'window_width': int(config['Settings']['window_width']),
            'window_height': int(config['Settings']['window_height']),
            'itemarea_displines': int(config['Settings']['itemarea_displines']),
            'scroll_lines': int(config['Settings']['scroll_lines']),
            'messages': config['Settings']['messages'],
            'autosave_json': config['Settings']['autosave_json'],
            'backup_json': config['Settings']['backup_json'],
            'textfont': config['Settings']['textfont'],
            'fontsize_treeview': int(config['Settings']['fontsize_treeview']),
            'fontsize_textbox': int(config['Settings']['fontsize_textbox']),
            'datetime_format': config['Settings']['datetime_format'],
            'multiple_boot': config['Settings']['multiple_boot'],
        }

        is_valid, errors = validate_settings(settings)
        if not is_valid:
            error_message = "\n".join([f"{key}: {value}" for key, value in errors.items()])
            messagebox.showerror("Configuration Error", error_message)
            sys.exit(1)

        # サニタイズと変数への代入
        global lang, increment_unit, window_width, window_height, itemarea_displines, scroll_lines
        global messages_enabled, autosave_json_enabled, backup_json, textfont
        global fontsize_treeview, fontsize_textbox, datetime_format, multiple_boot

        lang = sanitize_input(settings['lang'], 'str')
        increment_unit = sanitize_input(settings['increment_unit'], 'float')
        window_width = sanitize_input(settings['window_width'], 'int')
        window_height = sanitize_input(settings['window_height'], 'int')
        itemarea_displines = sanitize_input(settings['itemarea_displines'], 'int')
        scroll_lines = sanitize_input(settings['scroll_lines'], 'int')
        messages_enabled = sanitize_input(settings['messages'], 'bool')
        autosave_json_enabled = sanitize_input(settings['autosave_json'], 'bool')
        backup_json = sanitize_input(settings['backup_json'], 'str')
        textfont = sanitize_input(settings['textfont'], 'str')
        fontsize_treeview = sanitize_input(settings['fontsize_treeview'], 'int')
        fontsize_textbox = sanitize_input(settings['fontsize_textbox'], 'int')
        datetime_format = sanitize_input(settings['datetime_format'], 'str')
        multiple_boot = sanitize_input(settings['multiple_boot'], 'str')




    def start(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        # フォント設定(tkFontのインポートをrootウインドウ作成後に行う必要があるため、initではなくここで実施)
        global textfont
        textfont = config['Settings']['textfont']
        try:
            # システムにインストールされているフォント名一覧を取得
            available_fonts = tkFont.families()
            # 設定ファイルで指定されたフォント名が、システムにインストールされているかを確認
            if textfont == "TkDefaultFont" or textfont in available_fonts:
                # インストールされている場合は、指定されたフォントをそのまま使用
                pass
            else:
                # インストールされていない場合は、デフォルトフォントを使用
                textfont = 'TkDefaultFont'
                messagebox.showwarning("Font Warning", f"The specified font was not found. Using the default font.")

        except tk.TclError:
            textfont = 'TkDefaultFont'  # 利用できないフォントならTkinterのデフォルトフォントを使用
            messagebox.showwarning("Font Error", "An error occurred while setting the font. Using the default font.")

        self.root.mainloop()


    def on_shift_press(self, event):
        self.is_shift_pressed = True

    def on_shift_release(self, event):
        self.is_shift_pressed = False


    def focus_search_box(self, event=None):
        # Ctrl+Fを押したときにtext_box_searchにフォーカスを移し、
        # text_box_search内のテキストを全範囲選択
        self.text_box_search.focus_set()  # text_box_searchにフォーカス
        self.text_box_search.select_range(0, tk.END)  # テキストを全範囲選択
        return "break"  # イベントの伝播を停止


    def expand_selection(self, target_text):
        try:
            sel_start = target_text.index(tk.SEL_FIRST)
            sel_end = target_text.index(tk.SEL_LAST)
        except tk.TclError:
            # 選択範囲がない場合は何もしない
            return False

        # 行の内容を取得
        line_start = target_text.index(f"{sel_start} linestart")
        line_end = target_text.index(f"{sel_end} lineend")
        line_content = target_text.get(line_start, line_end)

        # 選択範囲の前後を検査
        start_offset = int(target_text.index(sel_start).split('.')[1])
        end_offset = int(target_text.index(sel_end).split('.')[1])
        before = line_content[:start_offset]
        after = line_content[end_offset:]

        # 括弧を探す
        open_paren = before.rfind('(')
        close_paren = after.find(')')

        if open_paren != -1 and close_paren != -1:
            # 開き括弧が見つからない場合（選択範囲が先頭から始まる場合）
            if open_paren == -1:
                new_start = line_start
            else:
                new_start = f"{line_start}+{open_paren}c"

            # 閉じ括弧が見つからない場合
            if close_paren == -1:
                new_end = line_end
            else:
                new_end = f"{sel_end}+{close_paren + 1}c"

            # 拡張後の内容を取得
            expanded_content = target_text.get(new_start, new_end)

            # ":数字" パターンをチェック
            match = re.search(r':([\d.]+)?\)$', expanded_content)
            if match:
                # ":数字" パターンが見つかった場合、それも含める
                new_end = f"{sel_end}+{close_paren + 1}c"

            target_text.tag_remove(tk.SEL, '1.0', tk.END)
            target_text.tag_add(tk.SEL, new_start, new_end)
            return True
        
        return False


    def on_ctrl_arrow_key(self, event):
        text_widget = event.widget
        
        try:
            start = text_widget.index(tk.SEL_FIRST)
            end = text_widget.index(tk.SEL_LAST)
            selected_text = text_widget.get(start, end)
        except tk.TclError:
            # return "break"  # 範囲指定されていない場合は何もせず、イベント伝播を停止
            # 選択範囲がない場合、カーソル位置の1単語を選択
            cursor_position = text_widget.index(tk.INSERT)
            word_start = text_widget.index(f"{cursor_position} wordstart")
            word_end = text_widget.index(f"{cursor_position} wordend")
            text_widget.tag_add(tk.SEL, word_start, word_end)  # 1単語を選択
            start = word_start
            end = word_end
            selected_text = text_widget.get(start, end)

        # 括弧で囲むか、数値を増減するかを判断
        if selected_text.startswith("(") and selected_text.endswith(")"):
            # 既に括弧で囲まれている場合、数値を増減
            new_text = self.modify_text(selected_text[1:-1], event.keysym == 'Up')
            text_widget.delete(start, end)
            text_widget.insert(start, f"({new_text})")
            # 選択範囲を維持
            text_widget.tag_add(tk.SEL, start, f"{start}+{len(new_text) + 2}c")
        else:
            # 選択範囲の拡張を試みる
            ret = self.expand_selection(text_widget)

            if ret==False:
                # 括弧で囲む
                new_text = f"({selected_text}:1.0)"
                text_widget.delete(start, end)
                text_widget.insert(start, new_text)
                # 選択範囲を維持
                text_widget.tag_add(tk.SEL, start, f"{start}+{len(new_text)}c")

        # カーソル位置を選択範囲の終わりに設定
        text_widget.mark_set(tk.INSERT, tk.SEL_LAST)
        # イベントの伝播を停止
        return "break"


    def modify_text(self, text, increase):
        # 数値部分を抽出
        match = re.search(r'^(.*?):(-?[\d.]+)$', text)
        if match:
            base_text = match.group(1)
            number = float(match.group(2))
        else:
            base_text = text
            number = 1.0

        # 数値を増減
        if increase:
            number += increment_unit
        else:
            number -= increment_unit

        # 数値のフォーマット
        if increment_unit == 0.1:
            number = round(number, 1)
        elif increment_unit == 0.05:
            number = round(number * 20) / 20  # 0.05単位で丸める
        else:
            number = round(number, 2)

        # 小数点以下の桁数を調整
        if number.is_integer():
            formatted_number = f"{number:.1f}"
        elif number * 10 % 1 == 0:
            formatted_number = f"{number:.1f}"
        else:
            formatted_number = f"{number:.2f}"

        new_text = f"{base_text}:{formatted_number}"
        return new_text


    def on_double_click(self, event):
        text_widget = event.widget
        
        # テキストウィジェットであることを確認
        # エラー抑止処理
        if not isinstance(text_widget, tk.Text):
            return  # テキストウィジェットでない場合は何もしない

        # 現在の選択範囲を取得
        try:
            start = text_widget.index(tk.SEL_FIRST)
            end = text_widget.index(tk.SEL_LAST)
        except tk.TclError:
            # 選択範囲がない場合は何もしない
            return

        # 選択されたテキストを取得
        selected_text = text_widget.get(start, end)

        # 選択範囲の先頭に"("があれば、それを選択範囲から除外
        if selected_text.startswith("("):
            selected_text = selected_text[1:]  # 先頭の"("を除外
            start = f"{start}+1c"  # 新しい開始位置を更新
            text_widget.mark_set(tk.INSERT, start)  # キャレットの位置を更新

        colon_index = selected_text.find(":")
        if colon_index != -1:
            selected_text = selected_text[:colon_index]  # ":"以降を除外
            end = start  # 新しい終了位置を開始位置に設定

        # 末尾のカンマやピリオドを除去
        cleaned_text = re.sub(r'[,.]+$', '', selected_text)  # 末尾のカンマやピリオドをすべて削除

        # 新しい終了位置を計算
        new_end = f"{start}+{len(cleaned_text)}c"

        # 選択範囲を更新
        text_widget.tag_remove(tk.SEL, "1.0", tk.END)
        text_widget.tag_add(tk.SEL, start, new_end)

        return "break"  # デフォルトの動作を防ぐ


    def on_tree_select(self, event):
        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            item_text = tree.item(selected_item[0], "text")
            parent_item = tree.parent(selected_item[0])
            if parent_item:
                self.text_box_top.delete(1.0, tk.END)
                self.text_box_top.insert(tk.END, item_text)
                self.text_box_top.focus()  # 選択時、アイテム欄にフォーカス
                self.last_selected_parent = selected_item[0]
                self.last_selected_child = parent_item
            else:
                self.text_box_top.delete(1.0, tk.END)
                self.text_box_top.insert(tk.END, item_text)
                self.text_box_top.focus()  # 選択時、アイテム欄にフォーカス
                self.last_selected_parent = selected_item[0]
                self.last_selected_child = None
            # ハイライト処理
            self.update_highlight()
        
        # 削除ボタンと更新ボタンの有効・無効切り替え
        if tree in [self.tree1, self.tree2]:
            self.delete_button.config(state=tk.NORMAL)
            self.update_button.config(state=tk.NORMAL)
        elif tree == self.tree3:
            if parent_item:  # 子アイテムが選択されている場合
                self.delete_button.config(state=tk.NORMAL)
                self.update_button.config(state=tk.NORMAL)
            else:  # 親アイテムが選択されている場合
                self.delete_button.config(state=tk.DISABLED)
                # self.update_button.config(state=tk.DISABLED)


    def expand_all(self):
        for tree in [self.tree1, self.tree2, self.tree3]:
            for item in tree.get_children():
                tree.item(item, open=True)
                self.expand_children(tree, item)


    def expand_children(self, tree, item):
        for child in tree.get_children(item):
            tree.item(child, open=True)
            self.expand_children(tree, child)


    def collapse_all(self):
        for tree in [self.tree1, self.tree2, self.tree3]:
            for item in tree.get_children():
                tree.item(item, open=False)
                self.collapse_children(tree, item)


    def collapse_children(self, tree, item):
        for child in tree.get_children(item):
            tree.item(child, open=False)
            self.collapse_children(tree, child)


    # ツリーアイテムを左クリックで選択したときの動作
    def on_tree_item_press(self, event):
        tree = event.widget
        self.drag_data = {"x": event.x, "y": event.y, "item": tree.identify_row(event.y), "tree": tree}
        self.is_dragging = True  # ドラッグ開始時に is_dragging を True に設定
        # ドラッグ開始時にアイテムを記録
        self.drag_start_item = self.drag_data["item"]

        # お気に入りタブの親アイテムの場合、ドラッグを禁止
        if tree == self.tree3 and not tree.parent(self.drag_start_item):
            self.is_dragging = False  # ドラッグを禁止
            self.drag_data = {}  # ドラッグデータをクリア


    # ツリーアイテムを右クリックで選択したときの動作
    def on_tree_item_press2(self, event):
        # 右クリックでアイテムを選択
        tree = event.widget
        item = tree.identify_row(event.y)

        if tree == self.tree1:
            if self.tree1.exists(item):
                self.tree1.selection_set(item)
        elif tree == self.tree2:
            if self.tree2.exists(item):
                self.tree2.selection_set(item)
        elif tree == self.tree3:
            if self.tree3.exists(item):
                self.tree3.selection_set(item)

        self.right_click_menu(event)


    def on_tree_item_motion(self, event):
        if "item" in self.drag_data and self.drag_data["item"]:
            x, y = event.x, event.y
            dx = abs(x - self.drag_data["x"])
            dy = abs(y - self.drag_data["y"])

            if dx > 16 or dy > 16:
                tree = self.drag_data["tree"]
                if tree != None:
                    target_item = tree.identify_row(y)
                    if target_item and target_item != self.drag_start_item:  # ドラッグ開始アイテムと異なる場合のみ移動
                        source_parent = tree.parent(self.drag_start_item)
                        target_parent = tree.parent(target_item)

                        # 子アイテムを持たない親アイテムの上に移動された場合
                        if target_parent == "" and not tree.get_children(target_item):
                            tree.move(self.drag_start_item, target_item, "end")  # 親アイテムの配下に移動
                            tree.item(target_item, open=True)  # 親アイテムを展開
                        elif (source_parent == "" and target_parent == "") or (source_parent != "" and target_parent != ""):
                            tree.move(self.drag_start_item, tree.parent(target_item), tree.index(target_item))

                self.drag_data["x"] = x
                self.drag_data["y"] = y


    def on_tree_item_release(self, event):
        # ドラッグ終了時のイベント処理
        if "item" in self.drag_data and self.drag_data["item"]:
            # ドラッグ移動の有無を判定
            if abs(event.x - self.drag_data["x"]) < 16 and abs(event.y - self.drag_data["y"]) < 16:
                # ドラッグ移動をしていない場合、アイテムを追加
                self.add_item_to_prompt(event)

                if autosave_json_enabled:
                    self.save_dicts_to_json()

            # ドラッグ終了後、変数をリセット
            self.drag_data = {"x": 0, "y": 0, "item": None, "tree": None}
            self.is_dragging = False  # ドラッグ終了時に is_dragging を False に設定


    def add_item_to_prompt(self, event):
        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            item_text = tree.item(selected_item[0], "text")
            parent_item = tree.parent(selected_item[0])
            if parent_item:
                # 子アイテムが選択された場合
                self.text_box_top.delete(1.0, tk.END)
                self.text_box_top.insert(tk.END, item_text)
                self.text_box_top.focus()  # 選択時、アイテム欄にフォーカス

                # 前回選択したアイテムと同じなら下部テキストボックスに追加
                if self.last_selected_child == selected_item[0]:
                    # コメント行("#"で始まる行)を除外
                    text_lines = item_text.split("\n")
                    filtered_lines = [line for line in text_lines if not line.startswith("#")]

                    # 行の途中から始まるコメントを改行部分まで除外
                    filtered_lines2 = ""
                    for line in filtered_lines:
                        if "#" in line:
                            _index = line.find('#')
                            if _index != -1:
                                line = line[:_index].strip()
                        filtered_lines2 += line + '\n'

                    # 末尾の余計な改行を削除
                    filtered_lines2 = filtered_lines2.rstrip('\n')
                    # 末尾に", "を追加
                    filtered_lines2 = filtered_lines2.rstrip(',') + ", "

                    cursor_position = self.text_box_bottom.index(tk.INSERT)
                    if cursor_position:
                        self.text_box_bottom.insert(cursor_position, filtered_lines2)
                    else:
                        self.text_box_bottom.insert(tk.END, filtered_lines2)
                    self.text_box_bottom.focus()  # アイテム追加後、プロンプト欄にフォーカス
                    self.save_to_history2()
                else:
                    self.last_selected_child = selected_item[0]
                    self.last_selected_parent = parent_item
            else:
                self.text_box_top.delete(1.0, tk.END)
                self.text_box_top.insert(tk.END, item_text)
                self.text_box_top.focus()  # 選択時、アイテム欄にフォーカス
                self.last_selected_parent = selected_item[0]
                self.last_selected_child = None
            # ハイライト処理
            self.update_highlight()


    # 右クリックメニュー
    def right_click_menu(self, event):
        menu = Menu(self.root, tearoff=0)
        current_tab = self.tab_control.index(self.tab_control.select())
        if current_tab == 0:
            tree = self.tree1
        elif current_tab == 1:
            tree = self.tree2
        elif current_tab == 2:
            tree = self.tree3
        else:
            tree = None

        selected_item = tree.selection()
        # チャンクタブか単語タブの場合
        if tree in [self.tree1, self.tree2]:
            if selected_item:
                parent_item = tree.parent(selected_item[0])
                if parent_item:  # 子アイテムが選択されている場合
                    menu.add_command(label=messages[lang]['button_copy_text'], command=self.copy_item_text)
                    menu.add_command(label=messages[lang]['button_clone_item'], command=lambda: self.clone_child_item(tree, selected_item))
                    menu.add_command(label=messages[lang]['button_add_fav'], command=self.add_to_favorites)
                    menu.add_command(label=messages[lang]['button_delete'], command=self.on_delete_button_click)
                else:  # 親アイテムが選択されている場合
                    menu.add_command(label=messages[lang]['button_copy_text'], command=self.copy_item_text)
                    menu.add_command(label=messages[lang]['button_delete'], command=self.on_delete_button_click)
            self.delete_button.config(state=tk.NORMAL)
            self.update_button.config(state=tk.NORMAL)

        # お気に入りタブの場合
        elif tree == self.tree3:
            if selected_item:
                parent_item = tree.parent(selected_item[0])
                if parent_item:  # 子アイテムが選択されている場合
                    menu.add_command(label=messages[lang]['button_copy_text'], command=self.copy_item_text)
                    menu.add_command(label=messages[lang]['button_delete'], command=self.on_delete_button_click)
                    self.delete_button.config(state=tk.NORMAL)
                    self.update_button.config(state=tk.NORMAL)
                else:  # 親アイテムが選択されている場合
                    self.delete_button.config(state=tk.DISABLED)
                    # self.update_button.config(state=tk.DISABLED)

        menu.post(event.x_root, event.y_root)


    def copy_item_text(self):
        current_tab = self.tab_control.index(self.tab_control.select())
        if current_tab == 0:
            tree = self.tree1
        elif current_tab == 1:
            tree = self.tree2
        elif current_tab == 2:
            tree = self.tree3
        else:
            tree = None

        if tree:
            selected_item = tree.selection()
            if selected_item:
                item_text = tree.item(selected_item[0], "text")
                self.root.clipboard_clear()
                self.root.clipboard_append(item_text)
                self.root.update()
                if messages_enabled:
                    messagebox.showinfo(messages[lang]['title_copy_complete'], messages[lang]['message_item_copied'])
            else:
                messagebox.showerror(messages[lang]['title_select_error'], messages[lang]['message_select_favitem'])


    def clone_child_item(self, tree, selected_item):
        if selected_item:
            parent_item = tree.parent(selected_item[0])
            if parent_item:
                # 選択されたアイテムのテキストを取得
                item_text = tree.item(selected_item, "text")

                # 選択されたアイテムの親を取得
                parent_item = tree.parent(selected_item)

                # 選択されたアイテムのインデックスを取得
                item_index = tree.index(selected_item)

                # 親アイテムの下に新しい子アイテムを挿入
                cloned_item = tree.insert(parent_item, item_index + 1, text=item_text)
                self.set_item_focus(tree, cloned_item)  # フォーカス移動

                if autosave_json_enabled:
                    self.save_dicts_to_json()
                if messages_enabled:
                    messagebox.showinfo(messages[lang]['title_clone_info'], messages[lang]['message_clone_complete'])


    # ツリー上の指定したアイテムを選択状態にしてフォーカスを移し、視認できるようにスクロールする
    def set_item_focus(self, tree, item):
        tree.selection_set(item)  # 追加したアイテムを選択状態にする
        tree.focus(item)  # 追加したアイテムにフォーカスを移す
        tree.see(item)  # 追加したアイテムが見えるようにスクロール


    def add_to_favorites(self):
        current_tab = self.tab_control.index(self.tab_control.select())
        if current_tab == 0:
            tree = self.tree1
        elif current_tab == 1:
            tree = self.tree2
        elif current_tab == 2:
            tree = self.tree3
        else:
            tree = None

        if tree:
            selected_item = tree.selection()
            if selected_item:
                item_text = tree.item(selected_item[0], "text")
                # tree1のアイテムを選択している場合
                if tree == self.tree1:
                    favorites_parent = self.tree3.get_children()[0]  # 1つ目の親アイテム
                # tree2のアイテムを選択している場合
                elif tree == self.tree2:
                    favorites_parent = self.tree3.get_children()[1]  # 2つ目の親アイテム
                else:
                    return

                # 子アイテムとして追加
                self.tree3.insert(favorites_parent, "end", text=item_text)
                if autosave_json_enabled:
                    self.save_dicts_to_json()
                if messages_enabled:
                    messagebox.showinfo(messages[lang]['title_fav_info'], item_text + messages[lang]['message_fav_complete'])
            else:
                messagebox.showerror(messages[lang]['title_select_error'], messages[lang]['message_select_favitem'])


    # お気に入りタブ選択時はボタンが無効化されるようにしてある(@on_tab_changed)ため、
    # 表示しているタブによる分岐処理は未記載
    def on_add_parent_button_click(self):
        current_tab = self.tab_control.index(self.tab_control.select())
        if current_tab == 0:
            tree = self.tree1
        elif current_tab == 1:
            tree = self.tree2
        elif current_tab == 2:
            tree = self.tree3
        else:
            tree = None
        
        parent_count = len(tree.get_children()) + 1
        parent_text = f"Genre {parent_count}" if current_tab == 0 else f"Category {parent_count}"
        parent_item = tree.insert("", "end", text=parent_text)
        
        # 小アイテムを3つ追加
        for child_count in range(1, 4):  # 1から3までのループ
            tree.insert(parent_item, "end", text=str(child_count))  # 子アイテムを追加
        
        tree.item(parent_item, open=True)  # 親アイテムを展開
        tree.selection_set(parent_item)  # 追加した親アイテムを選択状態にする
        # tree.selection_set(child_item)  # 子アイテムの選択を解除
        self.set_item_focus(tree, parent_item)  # フォーカス移動

        if autosave_json_enabled:
            self.save_dicts_to_json()


    # お気に入りタブ選択時はボタンが無効化されるようにしてある(@on_tab_changed)ため、
    # 表示しているタブによる分岐処理は未記載
    def on_add_child_button_click(self):
        current_tab = self.tab_control.index(self.tab_control.select())
        if current_tab == 0:
            tree = self.tree1
        elif current_tab == 1:
            tree = self.tree2
        elif current_tab == 2:
            tree = self.tree3
        else:
            tree = None
        
        selected_item = tree.selection()
        if not selected_item:
            if messages_enabled:
                messagebox.showinfo(messages[lang]['title_select_error'], messages[lang]['message_select_item_to_add'])
            return

        parent_item = tree.parent(selected_item[0])
        if parent_item:
            parent_item = parent_item
        else:
            parent_item = selected_item[0]

        children = tree.get_children(parent_item)
        child_count = len(children) + 1
        child_item = tree.insert(parent_item, "end", text=str(child_count))  # 子アイテムを追加
        tree.item(parent_item, open=True)  # 親アイテムを展開
        self.set_item_focus(tree, child_item)  # フォーカス移動

        if autosave_json_enabled:
            self.save_dicts_to_json()


    def on_delete_button_click(self):
        current_tab = self.tab_control.index(self.tab_control.select())
        if current_tab == 0:
            tree = self.tree1
        elif current_tab == 1:
            tree = self.tree2
        elif current_tab == 2:
            tree = self.tree3
        else:
            tree = None
        
        selected_item = tree.selection()
        if selected_item:
            # お気に入りタブのアイテム選択時
            if tree == self.tree3:
                parent_item = tree.parent(selected_item[0])
                if parent_item:  # 子アイテムが選択されている場合
                    result = messagebox.askokcancel(messages[lang]['title_delete_confirm'], messages[lang]['message_item_deleted'])
                    if result:
                        tree.delete(selected_item[0])
                        if autosave_json_enabled:
                            self.save_dicts_to_json()
                else:  # 親アイテムが選択されている場合
                    messagebox.showerror(messages[lang]['title_delete_error'], messages[lang]['message_favparent_deletion_error'])
                    return
            # それ以外のタブのアイテム選択時
            else:
                parent_item = tree.parent(selected_item[0])
                if parent_item:  # 子アイテム選択時
                    # 子アイテム0個を許容するように変更するためコメントアウト
                    # children = tree.get_children(parent_item)
                    # if len(children) == 1:
                    #     if messages_enabled:
                    #         messagebox.showinfo(messages[lang]['title_delete_error'], messages[lang]['message_parent_needs_child'])
                    #     return
                    # else:
                    result = messagebox.askokcancel(messages[lang]['title_delete_confirm'], messages[lang]['message_item_deleted'])
                    if result:
                        # 削除前に前後のアイテムを記憶しておく
                        previous_item = tree.prev(selected_item[0])
                        next_item = tree.next(selected_item[0])
                        # 削除したアイテムの上のアイテムにフォーカスを移動
                        if previous_item:
                            self.set_item_focus(tree, previous_item)  # フォーカス移動
                        else:
                            # 上のアイテムがない場合は下のアイテムにフォーカスを移動
                            if next_item:
                                self.set_item_focus(tree, next_item)  # フォーカス移動

                        tree.delete(selected_item[0])
                        if autosave_json_enabled:
                            self.save_dicts_to_json()
                else:  # 親アイテム選択時
                    children = tree.get_children(selected_item[0])
                    if len(tree.get_children()) == 1:
                        if messages_enabled:
                            messagebox.showinfo(messages[lang]['title_delete_error'], messages[lang]['message_parent_needs_one'])
                        return
                    elif children:
                        result = messagebox.askokcancel(messages[lang]['title_delete_confirm'], messages[lang]['message_item_deleted_with_children'])
                        if result:
                            # 削除前に前後のアイテムを記憶しておく
                            previous_item = tree.prev(selected_item[0])
                            next_item = tree.next(selected_item[0])
                            # 削除したアイテムの上のアイテムにフォーカスを移動
                            if previous_item:
                                self.set_item_focus(tree, previous_item)  # フォーカス移動
                            else:
                                # 上のアイテムがない場合は下のアイテムにフォーカスを移動
                                if next_item:
                                    self.set_item_focus(tree, next_item)  # フォーカス移動

                            tree.delete(selected_item[0])
                            if autosave_json_enabled:
                                self.save_dicts_to_json()
                    else:
                        # 削除前に前後のアイテムを記憶しておく
                        previous_item = tree.prev(selected_item[0])
                        next_item = tree.next(selected_item[0])
                        # 削除したアイテムの上のアイテムにフォーカスを移動
                        if previous_item:
                            self.set_item_focus(tree, previous_item)  # フォーカス移動
                        else:
                            # 上のアイテムがない場合は下のアイテムにフォーカスを移動
                            if next_item:
                                self.set_item_focus(tree, next_item)  # フォーカス移動

                        tree.delete(selected_item[0])
                        if autosave_json_enabled:
                            self.save_dicts_to_json()
        else:
            messagebox.showerror(messages[lang]['title_delete_error'], messages[lang]['message_select_item_to_delete'])
            return


    def on_update_button_click(self):
        current_tab = self.tab_control.index(self.tab_control.select())
        if current_tab == 0:
            tree = self.tree1
        elif current_tab == 1:
            tree = self.tree2
        elif current_tab == 2:
            tree = self.tree3
        else:
            tree = None
        
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror(messages[lang]['title_update_error'], messages[lang]['message_select_item'])
            return

        new_text = self.text_box_top.get(1.0, tk.END).strip()
        if not new_text:
            messagebox.showerror(messages[lang]['title_update_error'], messages[lang]['message_text_empty'])
            return

        parent_item = tree.parent(selected_item[0])
        if not parent_item:
            for item in tree.get_children():
                if item != selected_item[0] and tree.item(item, "text") == new_text:
                    messagebox.showerror(messages[lang]['title_update_error'], messages[lang]['message_item_exists'])
                    return

        tree.item(selected_item[0], text=new_text)
        if autosave_json_enabled:
            self.save_dicts_to_json()
        if messages_enabled:
            messagebox.showinfo(messages[lang]['title_update_complete'], messages[lang]['message_item_updated'])


    # コピー2処理を追加
    def on_copy2_button_click(self):
        selected_item = self.tree1.selection() or self.tree2.selection() or self.tree3.selection()
        if selected_item:
            item_text = self.text_box_top.get(1.0, tk.END).strip()
            self.root.clipboard_clear()
            self.root.clipboard_append(item_text)
            self.root.update()
            if messages_enabled:
                messagebox.showinfo(messages[lang]['title_copy_complete'], messages[lang]['message_item_copied'])


    def on_list_button_click(self):
        prompt_folder = 'prompt'
        files = glob(os.path.join(prompt_folder, "prompt_saved_*.txt"))
        
        if not files:
            messagebox.showerror(messages[lang]['title_prompt_error'], messages[lang]['message_prompt_listitem_notfound'])
            return

        # 最新の5つのファイルを取得
        files.sort(key=os.path.getctime, reverse=True)
        latest_files = files[:5]

        # 新しいウィンドウを作成
        self.list_window = tk.Toplevel(self.root)
        self.list_window.title("Saved Prompts")

        # ボタンを縦に並べるフレーム
        self.button_frame2 = tk.Frame(self.list_window)
        self.button_frame2.pack(padx=10, pady=10)

        # 各ファイルに対するボタンを作成
        for file in latest_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                button = tk.Button(self.button_frame2, text=content, command=lambda c=content: self.open_prompt(c), width=80)
                button.pack(pady=5)

        # ページ切り替えボタン用のフレームを作成
        self.page_button_frame = tk.Frame(self.list_window)
        self.page_button_frame.pack(side=tk.BOTTOM, pady=5)

        # ページ切り替えボタンの作成
        total_files = len(files)
        pages = (total_files - 1) // 5 + 1

        for i in range(pages):
            page_button = tk.Button(self.page_button_frame, text=str(i + 1), command=lambda p=i: self.load_page(files, p), width=3)
            page_button.pack(side=tk.LEFT, padx=5)

        # 閉じるボタンを右端に配置
        close_button = tk.Button(self.page_button_frame, text=messages[lang]['button_close'], command=self.list_window.destroy, width=self.button_width1)
        close_button.pack(side=tk.RIGHT, padx=5)


    def load_page(self, files, page):
        # ページに応じてファイルを表示
        start_index = page * 5
        end_index = start_index + 5
        latest_files = files[start_index:end_index]

        # 既存のボタンをクリア
        for widget in self.button_frame2.winfo_children():
            widget.destroy()

        # 新しいボタンを作成
        for file in latest_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                button = tk.Button(self.button_frame2, text=content, command=lambda c=content: self.open_prompt(c), width=80)
                button.pack(pady=5)

        # ページ切り替えボタンをクリア
        for widget in self.page_button_frame.winfo_children():
            widget.destroy()

        total_files = len(files)
        pages = (total_files - 1) // 5 + 1

        for i in range(pages):
            page_button = tk.Button(self.page_button_frame, text=str(i + 1), command=lambda p=i: self.load_page(files, p), width=3)
            page_button.pack(side=tk.LEFT, padx=5)

        # 閉じるボタンを右端に配置
        close_button = tk.Button(self.page_button_frame, text=messages[lang]['title_close'], command=self.list_window.destroy, width=self.button_width1)
        close_button.pack(side=tk.RIGHT, padx=5)


    def open_prompt(self, content):
        # プロンプトをテキストボックスに表示
        self.text_box_bottom.delete(1.0, tk.END)
        self.text_box_bottom.insert(tk.END, content)
        self.undo_history.append(content)
        self.text_box_bottom.event_generate("<<UpdateText>>")


    def on_load_button_click(self):
        from tkinter import filedialog
        
        default_directory = 'prompt'
        file_path = filedialog.askopenfilename(defaultextension=".txt", initialdir=default_directory, filetypes=[("Text files", "*.txt")])
        
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_box_bottom.delete(1.0, tk.END)
                self.text_box_bottom.insert(tk.END, content)
                self.undo_history.append(content)
                self.text_box_bottom.event_generate("<<UpdateText>>")
            if messages_enabled:
                messagebox.showinfo(messages[lang]['title_load'], messages[lang]['message_load'])


    def on_save_button_click(self):
        if not self.text_box_bottom.get(1.0, tk.END).strip():
            messagebox.showerror(messages[lang]['title_save_error'], messages[lang]['message_text_empty'])
            return
        
        from tkinter import filedialog
        import datetime
        
        default_directory = 'prompt'
        default_filename = f"prompt_saved_{datetime.datetime.now().strftime(datetime_format)}.txt"
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialdir=default_directory, initialfile=default_filename)
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                # file.write(self.text_box_bottom.get(1.0, tk.END).strip())
                file.write(self.text_box_bottom.get(1.0, tk.END))  # ファイル末尾の空白をそのまま残したいのでこちらを採用
            if messages_enabled:
                messagebox.showinfo(messages[lang]['title_save'], messages[lang]['message_save'])


    def on_copy_button_click(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_box_bottom.get(1.0, tk.END).strip())
        self.root.update()
        if messages_enabled:
            messagebox.showinfo(messages[lang]['title_copy_complete'], messages[lang]['message_prompt_copied'])


    def on_shuffle_button_click(self):
        # プロンプト欄のテキストを取得
        text = self.text_box_bottom.get("1.0", tk.END).strip()

        # 選択範囲があるか確認
        try:
            start = self.text_box_bottom.index(tk.SEL_FIRST)
            end = self.text_box_bottom.index(tk.SEL_LAST)
            selected_text = self.text_box_bottom.get(start, end)
            text_to_shuffle = selected_text
        except tk.TclError:
            start = "1.0"  # 選択範囲がない場合は全体を対象とする
            end = "end"
            text_to_shuffle = text

        # 括弧で囲まれた単語を分割
        words = self.split_words(text_to_shuffle)

        # 括弧が適切に閉じられていない場合は処理を終了
        if not words:
            # split_wordsのほうでメッセージ出すのでここはコメントアウト
            # messagebox.showerror(messages[lang]['title_format_error'], messages[lang]['messages_unbalanced_brackets'])
            return

        # 単語をシャッフル
        random.shuffle(words)

        # シャッフル後のテキストを結合
        shuffled_text = ", ".join(words).strip(", ")  # スペース区切りからカンマ区切りに変更し、末尾のカンマを削除

        # 複数のカンマを一つのカンマに置換
        shuffled_text = re.sub(r',+', ',', shuffled_text)

        # ", , "を", "に置換
        shuffled_text = re.sub(r',\s*,', ', ', shuffled_text)

        # 複数のスペースを一つのスペースに置換
        shuffled_text = re.sub(r'\s+', ' ', shuffled_text)

        # 末尾が単語で終わっている場合、", "を追加
        if shuffled_text:
            shuffled_text += ", "

        # 選択範囲がある場合は選択範囲を更新
        try:
            self.text_box_bottom.delete(start, end)
            self.text_box_bottom.insert(start, shuffled_text)
            self.text_box_bottom.tag_add(tk.SEL, start, f"{start}+{len(shuffled_text)}c")
        except tk.TclError:
            # 選択範囲がない場合は全体を更新
            self.text_box_bottom.delete("1.0", tk.END)
            self.text_box_bottom.insert(tk.END, shuffled_text)

        # 履歴を保存
        self.save_to_history2()


    def split_words(self, text):
        # 括弧で囲まれた単語を分割する関数
        words = []
        current_word = ""
        bracket_stack = []
        for char in text:
            if char in "({[<":
                bracket_stack.append(char)
                current_word += char
            elif char in ")}]>":
                if bracket_stack:
                    # 括弧の対応関係をチェック
                    if (bracket_stack[-1] == "(" and char == ")") or \
                       (bracket_stack[-1] == "{" and char == "}") or \
                       (bracket_stack[-1] == "[" and char == "]") or \
                       (bracket_stack[-1] == "<" and char == ">"):
                        bracket_stack.pop()
                        current_word += char
                    else:
                        # 括弧が閉じられていない場合はエラー処理
                        messagebox.showerror(messages[lang]['title_format_error'], messages[lang]['messages_unbalanced_brackets'])
                        return []  # 空のリストを返す
                else:
                    # 括弧が閉じられていない場合はエラー処理
                    messagebox.showerror(messages[lang]['title_format_error'], messages[lang]['messages_unbalanced_brackets'])
                    return []  # 空のリストを返す
            elif char == "," and not bracket_stack:
                words.append(current_word.strip())
                current_word = ""
            else:
                current_word += char

        if current_word:
            words.append(current_word.strip())

        # もし括弧が閉じられていない場合、最後の単語を追加
        if bracket_stack:
            messagebox.showerror(messages[lang]['title_format_error'], messages[lang]['messages_unbalanced_brackets'])
            return []  # 空のリストを返す

        return words


    def toggle_lock(self):
        if self.lock_var.get():
            self.text_box_bottom.config(state=tk.DISABLED)  # 編集不可にする
            self.list_button.config(state=tk.DISABLED)  # 一覧ボタンを無効にする
            self.load_button.config(state=tk.DISABLED)  # ロードボタンを無効にする
            self.shuffle_button.config(state=tk.DISABLED)  # シャッフルボタンを無効にする
            self.clear_button.config(state=tk.DISABLED)  # クリアボタンを無効にする
        else:
            self.text_box_bottom.config(state=tk.NORMAL)  # 編集可能にする
            self.list_button.config(state=tk.NORMAL)  # 一覧ボタンを有効にする
            self.load_button.config(state=tk.NORMAL)  # ロードボタンを有効にする
            self.shuffle_button.config(state=tk.NORMAL)  # シャッフルボタンを有効にする
            self.clear_button.config(state=tk.NORMAL)  # クリアボタンを有効にする


    def on_clear_button_click(self):
        result = messagebox.askokcancel(messages[lang]['title_clear_confirm'], messages[lang]['message_prompt_cleared'])
        if result:
            self.save_to_history1()
            self.text_box_bottom.delete(1.0, tk.END)


    def update_highlight(self, event=None):
        # イベントが発生したウィジェットを特定
        if event and event.widget in [self.text_box_top, self.text_box_bottom]:
            current_widget = event.widget
        else:
            current_widget = None

        text_widgets = [self.text_box_top, self.text_box_bottom]

        for widget in text_widgets:
            # 現在のウィジェットが指定されている場合は、そのウィジェットのみ更新
            if current_widget and widget != current_widget:
                continue

            # Entryウィジェットから検索テキストを取得
            input_text = self.text_box_search.get().strip()

            # プレースホルダーテキストの場合は空文字列として扱う
            if input_text == self.text_box_search.placeholder:
                input_text = ""

            # すべてのタグを削除
            widget.tag_remove("highlight", "1.0", tk.END)
            widget.tag_remove("selected", "1.0", tk.END)
            widget.tag_remove("selected_highlight", "1.0", tk.END)

            # 選択範囲の取得
            try:
                sel_start = widget.index(tk.SEL_FIRST)
                sel_end = widget.index(tk.SEL_LAST)
                widget.tag_add("selected", sel_start, sel_end)
            except tk.TclError:
                sel_start = sel_end = None

            # 検索文字列のハイライト
            if input_text:
                start_index = "1.0"
                while True:
                    start_index = widget.search(input_text, start_index, stopindex=tk.END)
                    if not start_index:
                        break
                    end_index = f"{start_index}+{len(input_text)}c"
                    widget.tag_add("highlight", start_index, end_index)
                    start_index = end_index

            # 選択範囲と検索ハイライトの重複を処理
            if sel_start and sel_end:
                highlight_ranges = widget.tag_ranges("highlight")
                for i in range(0, len(highlight_ranges), 2):
                    h_start, h_end = highlight_ranges[i], highlight_ranges[i + 1]

                    # インデックスを比較可能な形式に変換
                    sel_start_parts = list(map(int, widget.index(sel_start).split('.')))
                    sel_end_parts = list(map(int, widget.index(sel_end).split('.')))
                    h_start_parts = list(map(int, widget.index(h_start).split('.')))
                    h_end_parts = list(map(int, widget.index(h_end).split('.')))

                    # 開始位置の最大値と終了位置の最小値を計算
                    overlap_start_parts = max(sel_start_parts, h_start_parts)
                    overlap_end_parts = min(sel_end_parts, h_end_parts)

                    # 結果をTkinterのインデックス形式に戻す
                    overlap_start = f"{overlap_start_parts[0]}.{overlap_start_parts[1]}"
                    overlap_end = f"{overlap_end_parts[0]}.{overlap_end_parts[1]}"

                    if widget.compare(overlap_start, "<", overlap_end):
                        widget.tag_add("selected_highlight", overlap_start, overlap_end)

            # タグの優先順位とスタイルを設定
            widget.tag_raise("selected_highlight", "highlight")
            widget.tag_raise("selected_highlight", "selected")

            widget.tag_config("highlight", background="yellow", foreground="black")
            widget.tag_config("selected", background="SystemHighlight", foreground="SystemHighlightText")
            widget.tag_config("selected_highlight", background="red", foreground="white")

        # イベント処理後に更新を確実に行うため、afterメソッドを使用
        self.after_id = self.root.after(10, self.delayed_highlight_update)


    def delayed_highlight_update(self):
        # after_idをクリア
        if hasattr(self, 'after_id'):
            self.root.after_cancel(self.after_id)
            del self.after_id

        # 両方のテキストボックスに対して強制的に更新を行う
        self.update_highlight()


    def on_entry_change(*args):
        # エントリーの内容が変更されたときに呼び出される関数
        # content = entry.get()
        # if content != entry.placeholder:
        #     print(f"検索内容: {content}")
        pass


    def ensure_prompt_files_exist(self):
        # dict_chunks.jsonの存在チェックと作成
        if not os.path.exists('dict_chunks.json'):
            with open('dict_chunks.json', 'w', encoding='utf-8') as file:
                json.dump(initial_data_chunks, file, ensure_ascii=False, indent=4)
        else:
            pass

        # dict_words.jsonの存在チェックと作成
        if not os.path.exists('dict_words.json'):
            with open('dict_words.json', 'w', encoding='utf-8') as file:
                json.dump(initial_data_words, file, ensure_ascii=False, indent=4)
        else:
            pass

        if not os.path.exists('dict_favorites.json'):
            with open('dict_favorites.json', 'w', encoding='utf-8') as file:
                json.dump(initial_data_favorites, file, ensure_ascii=False, indent=4)

        # bkフォルダの存在チェックと作成
        if not os.path.exists('bk'):
            os.makedirs('bk')
        else:
            pass

        # promptフォルダの存在チェックと作成
        if not os.path.exists('prompt'):
            os.makedirs('prompt')
        else:
            pass

        # バックアップ設定の確認
        if backup_json == 'enable':
            # dict_chunks.jsonのバックアップ
            with open('dict_chunks.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            with open('bk/dict_chunks_bk.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            # dict_words.jsonのバックアップ
            with open('dict_words.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            with open('bk/dict_words_bk.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            # dict_favorites.jsonのバックアップ
            with open('dict_favorites.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            with open('bk/dict_favorites_bk.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)


    def load_dicts_from_json(self):
        # タブ1のツリービューをクリア
        for item in self.tree1.get_children():
            self.tree1.delete(item)

        # dict_chunks.jsonの読み込み
        with open('dict_chunks.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for parent, children in data.items():
                parent_item = self.tree1.insert("", "end", text=parent)
                for child in children:
                    self.tree1.insert(parent_item, "end", text=child)

        # タブ2のツリービューをクリア
        for item in self.tree2.get_children():
            self.tree2.delete(item)

        # dict_words.jsonの読み込み
        with open('dict_words.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for parent, children in data.items():
                parent_item = self.tree2.insert("", "end", text=parent)
                for child in children:
                    self.tree2.insert(parent_item, "end", text=child)

        for item in self.tree3.get_children():
            self.tree3.delete(item)

        # dict_favorites.jsonの読み込み
        with open('dict_favorites.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for parent, children in data.items():
                parent_item = self.tree3.insert("", "end", text=parent)
                for child in children:
                    self.tree3.insert(parent_item, "end", text=child)


    def save_dicts_to_json(self):
        try:
            # dict_chunks.jsonの保存
            data1 = {}
            for parent_item in self.tree1.get_children():
                parent_text = self.tree1.item(parent_item, "text")
                children_texts = [self.tree1.item(child, "text") for child in self.tree1.get_children(parent_item)]
                data1[parent_text] = children_texts

            with open('dict_chunks.json', 'w', encoding='utf-8') as file:
                json.dump(data1, file, ensure_ascii=False, indent=4)

            # dict_words.jsonの保存
            data2 = {}
            for parent_item in self.tree2.get_children():
                parent_text = self.tree2.item(parent_item, "text")
                children_texts = [self.tree2.item(child, "text") for child in self.tree2.get_children(parent_item)]
                data2[parent_text] = children_texts

            with open('dict_words.json', 'w', encoding='utf-8') as file:
                json.dump(data2, file, ensure_ascii=False, indent=4)

            # dict_favorites.jsonの保存
            data3 = {}
            for parent_item in self.tree3.get_children():
                parent_text = self.tree3.item(parent_item, "text")
                children_texts = [self.tree3.item(child, "text") for child in self.tree3.get_children(parent_item)]
                data3[parent_text] = children_texts

            with open('dict_favorites.json', 'w', encoding='utf-8') as file:
                json.dump(data3, file, ensure_ascii=False, indent=4)
            
            if not autosave_json_enabled:
                if messages_enabled:
                    messagebox.showinfo(messages[lang]['title_save_json'], messages[lang]['message_save_json_complete'])
        except Exception as e:
            messagebox.showerror(messages[lang]['title_save_json_error'], messages[lang]['message_save_json_notcomplete'] + str(e))


    def on_tab_changed(self, event):
        current_tab = self.tab_control.index(self.tab_control.select())
        if current_tab == 0:
            tree = self.tree1
        elif current_tab == 1:
            tree = self.tree2
        elif current_tab == 2:
            tree = self.tree3
        else:
            tree = None

        # ボタンの有効/無効を設定
        if current_tab == 2:  # tree3が表示中の場合
            self.add_parent_button.config(state=tk.DISABLED)
            self.add_child_button.config(state=tk.DISABLED)
        else:  # tree1またはtree2が表示中の場合
            self.add_parent_button.config(state=tk.NORMAL)
            self.add_child_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
            self.update_button.config(state=tk.NORMAL)

        selected_item = tree.selection()
        if selected_item:
            item_text = tree.item(selected_item[0], "text")
            self.text_box_top.delete(1.0, tk.END)
            self.text_box_top.insert(tk.END, item_text)

            if current_tab == 2:  # お気に入りタブの場合
                parent_item = tree.parent(selected_item[0])
                if not parent_item:  # 親アイテムが選択されている場合
                    self.delete_button.config(state=tk.DISABLED)
                    # self.update_button.config(state=tk.DISABLED)
                else:
                    self.delete_button.config(state=tk.NORMAL)
                    self.update_button.config(state=tk.NORMAL)
        else:
            self.text_box_top.delete(1.0, tk.END)

        # ハイライト処理
        self.update_highlight()


    def scroll_leftpane(self, event):
        tree = event.widget
        if event.delta < 0:
            tree.yview_scroll(scroll_lines-1, "units")
        elif event.delta > 0:
            tree.yview_scroll(-scroll_lines-1, "units")


    # Shift込みで監視している
    def on_mousewheel_leftpane(self, event):
        global rowheight_treeview

        if not event.delta < 0:
            self.fontsize_treeview_current -= 1
            self.fontsize_treeview_current = self.clamp(self.fontsize_treeview_current, fontsize_min, fontsize_max)
            rowheight_treeview = self.fontsize_treeview_current + 10
            style = ttk.Style()
            style.configure("Treeview", font=(textfont, self.fontsize_treeview_current), rowheight=rowheight_treeview)
            self.tree1.configure(style="Treeview")
            self.tree2.configure(style="Treeview")
            self.tree3.configure(style="Treeview")

        elif not event.delta > 0:
            self.fontsize_treeview_current += 1
            self.fontsize_treeview_current = self.clamp(self.fontsize_treeview_current, fontsize_min, fontsize_max)
            rowheight_treeview = self.fontsize_treeview_current + 10
            style = ttk.Style()
            style.configure("Treeview", font=(textfont, self.fontsize_treeview_current), rowheight=rowheight_treeview)
            self.tree1.configure(style="Treeview")
            self.tree2.configure(style="Treeview")
            self.tree3.configure(style="Treeview")


    # Shiftは監視していない(できない？)ので、Shift監視は別の処理で実施
    def on_mouseclick_leftpane(self, event):
        global rowheight_treeview

        if self.is_shift_pressed:  # Shiftキーが押されている場合
            # フォントサイズをini設定に戻す
            self.fontsize_treeview_current = fontsize_treeview
            self.fontsize_treeview_current = self.clamp(self.fontsize_treeview_current, fontsize_min, fontsize_max)
            rowheight_treeview = self.fontsize_treeview_current + 10
            style = ttk.Style()
            style.configure("Treeview", font=(textfont, self.fontsize_treeview_current), rowheight=rowheight_treeview)
            self.tree1.configure(style="Treeview")
            self.tree2.configure(style="Treeview")
            self.tree3.configure(style="Treeview")


    # Shift込みで監視している
    def on_mousewheel_rightpane(self, event):
        global fontsize_textbox

        if not event.delta < 0:
            self.fontsize_textbox_current -= 1
            self.fontsize_textbox_current = self.clamp(self.fontsize_textbox_current, fontsize_min, fontsize_max)
            fontsize_textbox = self.fontsize_textbox_current
            self.text_box_top.config(font=(textfont, self.fontsize_textbox_current))
            self.text_box_bottom.config(font=(textfont, self.fontsize_textbox_current))
            self.text_box_search.config(font=(textfont, self.fontsize_textbox_current))

        elif not event.delta > 0:
            self.fontsize_textbox_current += 1
            self.fontsize_textbox_current = self.clamp(self.fontsize_textbox_current, fontsize_min, fontsize_max)
            fontsize_textbox = self.fontsize_textbox_current
            self.text_box_top.config(font=(textfont, self.fontsize_textbox_current))
            self.text_box_bottom.config(font=(textfont, self.fontsize_textbox_current))
            self.text_box_search.config(font=(textfont, self.fontsize_textbox_current))


    # Shiftは監視していない(できない？)ので、Shift監視は別の処理で実施
    def on_mouseclick_rightpane(self, event):
        global fontsize_textbox

        if self.is_shift_pressed:  # Shiftキーが押されている場合
            # フォントサイズをini設定に戻す
            self.fontsize_textbox_current = fontsize_textbox
            self.fontsize_textbox_current = self.clamp(self.fontsize_textbox_current, fontsize_min, fontsize_max)
            fontsize_textbox = self.fontsize_textbox_current
            self.text_box_top.config(font=(textfont, self.fontsize_textbox_current))
            self.text_box_bottom.config(font=(textfont, self.fontsize_textbox_current))
            self.text_box_search.config(font=(textfont, self.fontsize_textbox_current))


    def clamp(self, value, vmin, vmax):
        return int(max(min(value, vmax), vmin))


    def load_latest_prompt_file(self):
        prompt_folder = 'prompt'
        if not os.path.exists(prompt_folder):  # フォルダの存在確認
            return

        pattern = os.path.join(prompt_folder, "prompt_tmp_*.txt")
        files = glob(pattern)

        if files:
            latest_file = max(files, key=os.path.getmtime)
            
            try:
                with open(latest_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if content.strip():  # 中身が空でないことを確認
                        self.text_box_bottom.delete(1.0, tk.END)
                        self.text_box_bottom.insert(tk.END, content)
                    self.undo_history.clear()
                    self.redo_history.clear()
                    self.undo_history.append(content)
            except Exception as e:
                print(f"Error reading file: {e}")  # エラーメッセージ


    # バインド用履歴保存処理(プロンプト欄の直接のテキスト編集を監視するのに使う)
    def save_to_history1(self, event=None):
        content = self.text_box_bottom.get("1.0", tk.END).strip()
        if not self.undo_history or content != self.undo_history[-1]:
            self.undo_history.append(content)
            self.redo_history.clear()

    # 普通呼び出し用履歴保存処理(ツリーからのアイテム選択によるチャンク・単語追加時に使う)
    def save_to_history2(self):
        content = self.text_box_bottom.get("1.0", tk.END).strip()
        if not self.undo_history or content != self.undo_history[-1]:
            self.undo_history.append(content)
            self.redo_history.clear()

    def undo(self, event=None):
        if len(self.undo_history) > 1:
            self.redo_history.append(self.undo_history.pop())
            self.text_box_bottom.delete("1.0", tk.END)
            self.text_box_bottom.insert(tk.END, self.undo_history[-1])
            self.text_box_bottom.event_generate("<<UpdateText>>")

    def redo(self, event=None):
        if self.redo_history:
            self.undo_history.append(self.redo_history.pop())
            self.text_box_bottom.delete("1.0", tk.END)
            self.text_box_bottom.insert(tk.END, self.undo_history[-1])
            self.text_box_bottom.event_generate("<<UpdateText>>")


    def toggle_autosave_json(self):
        global autosave_json_enabled
        autosave_json_enabled = self.autosave_json_var.get()
        config['Settings']['autosave_json'] = 'enable' if autosave_json_enabled else 'disable'
        with open(settings_path, 'w') as configfile:
            config.write(configfile)


    def save_prompt_and_close(self):
        import datetime
        import glob

        # 古いtmpファイルを削除
        old_files = glob.glob('prompt/prompt_tmp_*.txt')
        for old_file in old_files:
            os.remove(old_file)

        default_directory = 'prompt'
        default_filename = f"prompt_tmp_{datetime.datetime.now().strftime(datetime_format)}.txt"
        file_path = os.path.join(default_directory, default_filename)

        content = self.text_box_bottom.get(1.0, tk.END)  # 末尾の空白を残すためにrstripしない
        # 末尾の改行を一つだけに置換
        content = content.rstrip("\n") + "\n" if content.endswith("\n") else content

        # ここで内容が空の場合は完全に空にする
        if not content.strip():  # strip()で空白と改行を削除して判定
            self.text_box_bottom.delete(1.0, tk.END)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)  # ファイルに内容を書き込む
        
        # 少し待ってからウィンドウを閉じる
        self.root.after(100, self.root.destroy)


    def open_settings(self):
        # 設定ウィンドウを開く
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = settings(self)
        # 新しく開いたウインドウを排他的に操作できるようにする処理はsettingsのほうに記載


    def update_autosave_settings(self):
        """設定ファイルから自動保存設定を読み込み、変数とチェックボックスを更新する"""
        global autosave_json_enabled
        autosave_json_enabled = config['Settings'].get('autosave_json', 'enable') == 'enable'
        self.autosave_json_var.set(autosave_json_enabled)


    def on_exit(self, event=None):
        if not autosave_json_enabled:
            result = messagebox.askokcancel(messages[lang]['title_exit_confirm'], messages[lang]['message_autosave_disabled_confirm'])
            if result:
                # プロンプト欄が空でもtmpファイル作る
                self.save_prompt_and_close()

                if os.path.exists(lock_file_path):
                    os.remove(lock_file_path)  # ロックファイルを削除

                self.root.destroy()
            else:
                return
        else:
            # 終了時も辞書ファイル保存
            self.save_dicts_to_json()

            # 空でもtmpファイル作る
            self.save_prompt_and_close()
            os.remove(lock_file_path)  # ロックファイルを削除
            self.root.destroy()


# 検索欄監視用拡張
class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()


if __name__ == "__main__":
    PromptConstructorMain()

