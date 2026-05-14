import reflex as rx

def stock_card(title: str, count: int, icon: str, color: str) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon(tag=icon, color=color, size=20),
            rx.spacer(),
            rx.text(str(count), color="green", font_size="0.8em"),
            width="100%",
        ),
        rx.text(title, font_size="1.2em", font_weight="bold", color="gold"),
        rx.button(
            "Gestionar",
            width="100%",
            bg="rgba(255, 255, 255, 0.1)",
            color="white",
            _hover={"bg": "rgba(255, 255, 255, 0.2)"},
        ),
        padding="1.5em",
        border="1px solid rgba(255, 215, 0, 0.3)",
        border_radius="10px",
        bg="#1a1a1a",
        width="100%",
    )