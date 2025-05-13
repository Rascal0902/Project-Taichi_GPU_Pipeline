from PIL import Image

def convert_32bit_to_24bit_png(input_path, output_path):
    """32비트 PNG 이미지를 읽어 24비트 PNG로 변환합니다.

    Args:
        input_path: 입력 32비트 PNG 파일 경로.
        output_path: 출력 24비트 PNG 파일 경로.
    """
    try:
        # 이미지를 엽니다.
        img = Image.open(input_path)

        # 이미지 모드를 확인합니다.
        if img.mode == "RGBA":
            # RGBA 모드인 경우 RGB 모드로 변환합니다.
            rgb_img = img.convert("RGB")

            # 24비트 PNG로 저장합니다.
            rgb_img.save(output_path, "PNG")
            print(f"변환 완료: {output_path}")

        elif img.mode == "RGB":
            print(f"이미지는 이미 24비트입니다. 변환 없이 저장합니다: {output_path}")
            img.save(output_path, "PNG")

        else:
            print(f"지원하지 않는 이미지 모드입니다: {img.mode}")

    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다: {input_path}")
    except Exception as e:
        print(f"오류 발생: {e}")

# 사용 예시
input_file = "./inputs/sprite1.png"  # 32비트 PNG 파일 경로
output_file = "./inputs/test.png" # 출력 24비트 PNG 파일 경로

convert_32bit_to_24bit_png(input_file, output_file)