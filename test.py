import pygame
import sys

# Pygameの初期化
pygame.init()

# 画面サイズと色の設定
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("文字入力デモ")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# フォントの設定
font = pygame.font.Font(None, 36)

# 入力された文字列を保存する変数
user_text = ""

# メインループ
while True:
    screen.fill(WHITE)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]  # 最後の文字を削除
            elif event.key == pygame.K_RETURN:
                print("入力されたテキスト:", user_text)  # Enterが押されたときにテキストを出力
                user_text = ""  # 入力をリセット
            else:
                user_text += event.unicode  # その他のキーで文字を追加

    # テキストを画面に描画
    text_surface = font.render(user_text, True, BLACK)
    screen.blit(text_surface, (50, 100))

    # 画面更新
    pygame.display.flip()
