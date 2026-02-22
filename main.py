import flet as ft

# 데이터 정의 (기존과 동일)
types_18 = ["노말", "불꽃", "물", "풀", "전기", "얼음", "격투", "독", "땅", 
            "비행", "에스퍼", "벌레", "바위", "고스트", "드래곤", "악", "강철", "페어리"]

defense_chart = {
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

attack_strengths = {
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
    page.title = "포켓몬 상성 도우미"
    page.theme_mode = "dark" # 문자열로 설정
    page.padding = 20
    page.scroll = "adaptive"

    type_input = ft.TextField(
        label="타입 입력 (예: 물 비행)",
        hint_text="띄어쓰기로 구분",
        border_radius=10
    )
    
    result_col = ft.Column(spacing=10)

    def create_result_card(title, types, color_str):
        if not types: return ft.Container()
        # ft.colors.with_opacity 대신 직접 투명도가 포함된 색상 코드나 단순 이름을 사용
        return ft.Container(
            content=ft.Column([
                ft.Text(title, weight="bold", color=color_str, size=16),
                ft.Text(", ".join(types), size=14, color="white")
            ]),
            padding=15,
            bgcolor="black", # 가장 안전한 배경색
            border_radius=10,
            border=ft.border.all(1, color_str)
        )

    def calculate(e):
        result_col.controls.clear()
        raw_input = type_input.value.strip().split()
        targets = [t for t in raw_input if t in types_18]

        if not targets:
            result_col.controls.append(ft.Text("❌ 올바른 타입을 입력하세요.", color="red"))
            page.update()
            return

        multipliers = {t: 1.0 for t in types_18}
        for t in targets:
            chart = defense_chart[t]
            for w in chart["weak"]: multipliers[w] *= 2.0
            for r in chart["resist"]: multipliers[r] *= 0.5
            for z in chart["zero"]: multipliers[z] *= 0.0

        res = {4.0: [], 2.0: [], 0.5: [], 0.25: [], 0.0: []}
        for t, m in multipliers.items():
            if m in res: res[m].append(t)

        atk_s = set()
        for t in targets: atk_s.update(attack_strengths[t])

        result_col.controls.append(ft.Text(f"📊 {' + '.join(targets)} 분석", size=20, weight="bold"))
        result_col.controls.append(create_result_card("⚔️ 자속 공격 유리 (x2.0)", list(atk_s), "orange"))
        result_col.controls.append(create_result_card("💀 치명적 약점 (x4.0)", res[4.0], "red"))
        result_col.controls.append(create_result_card("⚠️ 주요 약점 (x2.0)", res[2.0], "pink"))
        result_col.controls.append(create_result_card("🚫 무효 (x0.0)", res[0.0], "grey"))
        result_col.controls.append(create_result_card("✅ 반감 (x0.5)", res[0.5], "green"))
        result_col.controls.append(create_result_card("💎 강한 반감 (x0.25)", res[0.25], "cyan"))
        page.update()

    page.add(
        ft.Text("포켓몬 상성 계산기", size=28, weight="bold"),
        type_input,
        ft.ElevatedButton("계산하기", on_click=calculate, width=400),
        result_col
    )

if __name__ == "__main__":
    ft.app(target=main)