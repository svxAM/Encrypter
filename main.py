import flet as ft
from flet.security import encrypt
import json

# ----- import config data -----

with open('config.json', 'r') as cfg_file:
    cfg = json.load(cfg_file)

# ----- global variables -----

isSelected = False
file_path = ''
file_name = ''
file_data = ''
encrypted_file_data = ''


# ----- main app -----

def main(page: ft.Page):
    # ----- page settings -----

    page.title = 'Encrypter'
    page.theme_mode = cfg['theme_mode']
    page.window.height = cfg['window_height']
    page.window.width = cfg['window_width']
    page.theme = ft.Theme(color_scheme_seed="cyan")
    page.bgcolor = "white"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # ----- functions -----

    def encrypt_and_output(e):
        global encrypted_file_data, isSelected

        if isSelected:
            key = key_field.value
            encrypted_file_data = encrypt(file_data, key)

            with open(f'{cfg['output_directory']}encrypted_{file_name}', 'w') as enc_file:
                enc_file.write(encrypted_file_data)

            snack_bar = ft.SnackBar(ft.Text('File encrypted and outputted!'))
            snack_bar.open = True
            snack_bar.bgcolor = 'green'
            page.overlay.append(snack_bar)

        else:
            snack_bar = ft.SnackBar(ft.Text('Error: File not selected'))
            snack_bar.open = True
            snack_bar.bgcolor = 'red'
            page.overlay.append(snack_bar)

        page.update()

    def pick_file(e: ft.FilePickerResultEvent):
        global file_data, file_path, file_name, isSelected

        files = e.files
        if files:
            isSelected = True
            file_path = files[0].path
            with open(file_path, 'r') as file:
                file_data = file.read()
            file_name = file_path[file_path.rfind('\\') + 1::]
            snack_bar = ft.SnackBar(ft.Text('File selected!'))
            snack_bar.open = True
            snack_bar.bgcolor = 'green'
            page.overlay.append(snack_bar)
        page.update()

    # ----- page controls -----

    file_pick_dialog = ft.FilePicker(on_result=pick_file)

    file_pick_button = ft.OutlinedButton(text='Select file',
                                         on_click=lambda e: file_pick_dialog.pick_files(allow_multiple=False),
                                         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),
                                                              side=ft.BorderSide(width=2))
                                         )

    encrypt_button = ft.FilledButton(text='Encrypt', on_click=encrypt_and_output, width=270, height=40,
                                     style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))

    key_field = ft.TextField(height=40, width=150, border_width=2, border_radius=10,
                             text_vertical_align=ft.VerticalAlignment.CENTER,
                             content_padding=ft.padding.symmetric(horizontal=10),
                             label="Key word",
                             password=True, can_reveal_password=True)

    # ----- page view -----

    page.overlay.append(file_pick_dialog)
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Image(src="icon.jpg", height=200, width=200)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Text(),
                ft.Text(),
                ft.Row(
                    [
                        file_pick_button,
                        key_field
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        encrypt_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    )


if __name__ == '__main__':
    ft.app(main)
