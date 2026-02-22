import flet as ft

# 1. 데이터 정의
TYPES = ["노말", "불꽃", "물", "풀", "전기", "얼음", "격투", "독", "땅", 
         "비행", "에스퍼", "벌레", "바위", "고스트", "드래곤", "악", "강철", "페어리"]

W, R, Z = 1.6, 0.625, 0.390625

DEFENSE_CHART = {
    "노말": {"weak": ["격투"], "resist": [], "zero": ["고스트"]},
    "불꽃": {"weak": ["물", "땅", "바위"], "resist": ["불꽃", "풀", "얼음", "벌레", "강철", "페어리"], "zero": []},
    "물": {"weak": ["풀", "전기"], "resist": ["불꽃", "물", "얼음", "강철"], "zero": []},
    "풀": {"weak": ["불꽃", "얼음", "독", "비행", "벌레"], "resist": ["물", "풀", "전기", "땅"], "zero": []},
    "전기": {"weak": ["땅"], "resist": ["전기", "비행", "강철"], "zero": []},
    "얼음": {"weak": ["불꽃", "격투", "바위", "강철"], "resist": ["얼음"], "zero": []},
    "격투": {"weak": ["비행", "에스퍼", "페어리"], "resist": ["벌레", "바위", "악"], "zero": []},
    "독": {"weak": ["땅", "에스퍼"], "resist": ["풀", "격투", "독", "벌레", "페어리"], "zero": []},
    "땅": {"weak": ["물", "풀", "얼음"], "resist": ["독", "바위"], "zero": ["전기"]},
    "비행": {"weak": ["전기", "얼음", "바위"], "resist": ["풀", "격투", "벌레"], "zero": ["땅"]},
    "에스퍼": {"weak": ["벌레", "고스트", "악"], "resist": ["격투", "에스퍼"], "zero": []},
    "벌레": {"weak": ["불꽃", "비행", "바위"], "resist": ["풀", "격투", "땅"], "zero": []},
    "바위": {"weak": ["물", "풀", "격투", "땅", "강철"], "resist": ["노말", "불꽃", "독", "비행"], "zero": []},
    "고스트": {"weak": ["고스트", "악"], "resist": ["독", "벌레"], "zero": ["노말", "격투"]},
    "드래곤": {"weak": ["얼음", "드래곤", "페어리"], "resist": ["불꽃", "물", "풀", "전기"], "zero": []},
    "악": {"weak": ["격투", "벌레", "페어리"], "resist": ["고스트", "악"], "zero": ["에스퍼"]},
    "강철": {"weak": ["불꽃", "격투", "땅"], "resist": ["노말", "풀", "얼음", "비행", "에스퍼", "벌레", "바위", "드래곤", "강철", "페어리"], "zero": ["독"]},
    "페어리": {"weak": ["독", "강철"], "resist": ["격투", "벌레", "악"], "zero": ["드래곤"]}
}

ATTACK_STRENGTHS = {
    "노말": [], "불꽃": ["풀", "얼음", "벌레", "강철"], "물": ["불꽃", "땅", "바위"],
    "풀": ["물", "땅", "바위"], "전기": ["물", "비행"], "얼음": ["풀", "땅", "비행", "드래곤"],
    "격투": ["노말", "얼음", "바위", "악", "강철"], "독": ["풀", "페어리"],
    "땅": ["불꽃", "전기", "독", "바위", "강철"], "비행": ["풀", "격투", "벌레"],
    "에스퍼": ["격투", "독"], "벌레": ["풀", "에스퍼", "악"],
    "바위": ["불꽃", "얼음", "비행", "벌레"], "고스트": ["에스퍼", "고스트"],
    "드래곤": ["드래곤"], "악": ["에스퍼", "고스트"],
    "강철": ["얼음", "바위", "페어리"], "페어리": ["격투", "드래곤", "악"]
}

def main(page: ft.Page):
    page.title = "포켓몬 GO 상성 계산기"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 450
    page.window.height = 850
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 20

    selected_types = []
    result_container = ft.Column(spacing=10)
    attack_info = ft.Text("", size=14, color=ft.Colors.BLUE_200)

    def update_result():
        result_container.controls.clear()
        if not selected_types:
            attack_info.value = ""
            page.update()
            return

        multipliers = {t: 1.0 for t in TYPES}
        for t in selected_types:
            chart = DEFENSE_CHART[t]
            for w in chart["weak"]: multipliers[w] *= W
            for r in chart["resist"]: multipliers[r] *= R
            for z in chart["zero"]: multipliers[z] *= Z

        atk_s = set()
        for t in selected_types: atk_s.update(ATTACK_STRENGTHS[t])
        attack_info.value = f"⚔️ 자속 보정 공격 강점: {', '.join(atk_s) if atk_s else '없음'}"

        sorted_res = sorted(multipliers.items(), key=lambda x: x[1], reverse=True)
        for t, m in sorted_res:
            if 0.99 <= m <= 1.01: continue
            
            # 아이콘 이름 변경: SHIELD_SHAPED -> SHIELD 등으로 교체
            if m > 2.0:
                color, label, icon = ft.Colors.RED_900, "치명적 약점", ft.Icons.GPP_BAD
            elif m > 1.0:
                color, label, icon = ft.Colors.RED_400, "약점", ft.Icons.WARNING_ROUNDED
            elif m < 0.5:
                color, label, icon = ft.Colors.BLUE_900, "최강 내성", ft.Icons.SHIELD
            else:
                color, label, icon = ft.Colors.BLUE_400, "내성", ft.Icons.SHIELD_OUTLINED

            result_container.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Row([ft.Icon(icon, color=color, size=20), ft.Text(f" {t}", weight="bold")]),
                        ft.Text(f"{label} (x{m:.3f})", color=color, weight="bold")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=12,
                    bgcolor=ft.Colors.with_opacity(0.1, color),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.3, color)),
                    border_radius=10
                )
            )
        page.update()

    def on_type_click(e):
        t = e.control.data
        if t in selected_types:
            selected_types.remove(t)
            e.control.bgcolor = ft.Colors.GREY_800
        else:
            if len(selected_types) >= 2: return
            selected_types.append(t)
            e.control.bgcolor = ft.Colors.BLUE_700
        
        selected_text.value = f"선택된 타입: {' / '.join(selected_types)}" if selected_types else "타입을 선택해 주세요 (최대 2개)"
        update_result()

    selected_text = ft.Text("타입을 선택해 주세요 (최대 2개)", size=16, weight="w600")
    
    type_grid = ft.GridView(
        expand=False,
        runs_count=3,
        max_extent=130,
        child_aspect_ratio=2.2,
        spacing=8,
    )

    for t in TYPES:
        type_grid.controls.append(
            ft.Container(
                content=ft.Text(t, weight="bold", color=ft.Colors.WHITE),
                alignment=ft.Alignment(0, 0),
                bgcolor=ft.Colors.GREY_800,
                border_radius=8,
                on_click=on_type_click,
                data=t,
            )
        )

    page.add(
        ft.Text("POKÉMON GO", size=28, weight="black", color=ft.Colors.BLUE_400),
        ft.Text("Type Effectiveness Calculator", size=14, color=ft.Colors.GREY_400),
        ft.Divider(height=30, color=ft.Colors.GREY_800),
        selected_text,
        ft.Container(type_grid, margin=ft.margin.only(top=10, bottom=10)),
        attack_info,
        ft.Divider(height=30, color=ft.Colors.GREY_800),
        ft.Text("🛡️ 방어 상성 분석", size=18, weight="bold"),
        result_container
    )

if __name__ == "__main__":
    ft.app(target=main)