import flet as ft
from countdown_timer import CountdownTimer
from countdown_timer import format_seconds
import os
import random
from math import pi

music = []
with os.scandir("assets/music") as entries:
    for entry in entries:
        if entry.is_file():
            music.append(entry.name)

images = []
with os.scandir("assets/images") as entries:
    for entry in entries:
        if entry.is_file():
            images.append(entry.name.removesuffix(".jpg"))


def main(page: ft.Page):
    page.title = "Focal"
    page.padding = 0
    page.window_title_bar_buttons_hidden = True
    page.window_title_bar_hidden = True
    page.theme = ft.Theme(color_scheme_seed="green")
    page.window_min_height = 1000
    page.window_min_width = 1000
    page.window_center()

    audio1 = ft.Audio(
        src=f"/music/{random.choice(music)}", autoplay=False
    )
    page.overlay.append(audio1)

    def close_menu(e):
        settings_menu.open = False
        page.update()

    def change_background(e):
        app_container.image_src = f"/images/{background_picker.value}.jpg"
        page.update()

    background_picker = ft.Dropdown(
        options=[ft.dropdown.Option(
            image
        ) for image in images],
        width=270,
        value=images[0],
        on_change=change_background
    )

    title_bar = ft.WindowDragArea(
        content=ft.Container(
            alignment=ft.alignment.center_right,
            padding=0,
            expand=True,
            height=28,
            content=ft.IconButton(
                icon=ft.icons.CLOSE_SHARP,
                icon_size=14,
                icon_color=ft.colors.WHITE,
                style=ft.ButtonStyle(
                    overlay_color=ft.colors.TRANSPARENT,
                    bgcolor={"hovered": ft.colors.RED},
                    shape=ft.RoundedRectangleBorder(radius=0)
                ),
                on_click=lambda _: page.window_close()
            )
        )
    )

    def update_session_duration(e):
        timer.stop()
        timer.reset()
        timer.seconds = int(timer_setter.value)*60
        timer.value = format_seconds(timer.seconds)
        timer.update()

    timer_setter = ft.TextField(
        width=100,
        value=25,
        on_submit=update_session_duration,
    )

    def increment(e):
        timer_setter.value = int(timer_setter.value)
        timer_setter.value += 5
        if timer_setter.value > 240:
            timer_setter.value = 240
        timer_setter.update()

    def decrement(e):
        timer_setter.value = int(timer_setter.value)
        timer_setter.value -= 5
        if timer_setter.value <= 0:
            timer_setter.value = 5
        timer_setter.update()

    settings_menu = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.IconButton(
                icon=ft.icons.CLOSE, 
                icon_color="#ffffff", 
                icon_size=25,
                on_click=close_menu
            ),
            ft.Text("Settings", size=25)
        ]),
        content=ft.Container(
            width=300,
            height=300,
            content=ft.Column([
                ft.Text("Background image:"),
                background_picker,
                ft.Text("Timer Duration"),
                ft.Row([
                    timer_setter,
                    ft.Column([
                        ft.IconButton(icon=ft.icons.ADD, on_click=increment),
                        ft.IconButton(icon=ft.icons.REMOVE, on_click=decrement)
                    ])
                ])
            ]),  
        ),
        actions=[
            ft.ElevatedButton(text="Save Changes", on_click=update_session_duration)
        ]
    )

    def open_settings(e):
        page.dialog = settings_menu
        settings_menu.open = True
        page.update()

    settings_btn = ft.IconButton(
        icon=ft.icons.SETTINGS_ROUNDED,
        icon_color=ft.colors.WHITE,
        style=ft.ButtonStyle(
            surface_tint_color=ft.colors.TRANSPARENT,
            bgcolor={"hovered": ft.colors.with_opacity(0.3, ft.colors.WHITE)}
        ),
        on_click=open_settings
    )

    timer = CountdownTimer()

    def start_countdown(e):
        timer.start()
        audio1.play()
        start_btn.icon = ft.icons.STOP_ROUNDED
        start_btn.text = "Stop"
        start_btn.on_click = stop
        page.update()

    def pause_coutdown(e):
        timer.pause()

    #def resume_countdown(e):
    #    timer.resume()

    def reset(e):
        restart_btn.rotate -= pi*2
        audio1.pause()
        timer.reset(int(timer_setter.value*60))
        page.update()

    def stop(e):
        timer.stop()
        audio1.pause()
        start_btn.on_click=start_countdown
        start_btn.icon = None
        start_btn.text = "Start"
        page.update()

    pause_btn = ft.IconButton(
        icon=ft.icons.PAUSE_ROUNDED,
        icon_color=ft.colors.WHITE,
        style=ft.ButtonStyle(
            side=ft.BorderSide(1.5, "#ffffff")
        ),
        on_click=pause_coutdown
    )

    start_btn = ft.ElevatedButton(
        icon_color=ft.colors.BLACK,
        height=45,
        text="Start",
        style=ft.ButtonStyle(
            bgcolor="#ffffff",
            color=ft.colors.BLACK
        ),
        on_click=start_countdown
    )

    restart_btn = ft.IconButton(
        icon=ft.icons.RESTART_ALT_ROUNDED,  
        icon_color=ft.colors.WHITE,
        style=ft.ButtonStyle(
            side=ft.BorderSide(1.5, "#ffffff")
        ),
        rotate=0,
        animate_rotation=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        on_click=reset
    )

    timer_controls = ft.Row([
        pause_btn,
        start_btn,
        restart_btn
    ], alignment=ft.MainAxisAlignment.CENTER)

    app = ft.Container(
        expand=True,
        padding=25,
        content=ft.Column([
            ft.Row([
                settings_btn
            ], alignment=ft.MainAxisAlignment.END),
            ft.Column([
                ft.Row([
                    ft.Stack([
                        ft.Container(timer, alignment=ft.alignment.center),
                    ], width=382, height=382)  
                ], alignment=ft.MainAxisAlignment.CENTER),
                timer_controls
            ], spacing=40)
        ])
    )

    app_container = ft.Container(
        expand=True,
        image_src="/images/Aerial Forest View.jpg",
        image_fit=ft.ImageFit.COVER,
        content=ft.Column([
            title_bar,
            app
        ])
    )

    page.add(app_container)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")

#TODO: Add a Progress Ring around the countdown
