import re
from library.kr2num import kr2num
from library.num2kr import num2kr

def extract_style(sentence):
    # 패턴 정의
    keyword_pattern = r'디자인|유행|스타일|트렌드'
    style_pattern = r'(모던|미니멀리즘|스칸디나비아|인더스트리얼|컨트리|클래식|빈티지|프렌치 프로방스|보헤미안|전통)'

    # 키워드가 포함된 문장을 찾습니다.
    if re.search(keyword_pattern, sentence):
        matches = re.findall(style_pattern, sentence)
        if matches:
            # 매치된 스타일 중 마지막 단일 값을 반환
            return matches[-1]
        else:
            return "None"
    else:
        return "None"

# budget
def extract_budget(sentence):
    numeric_budget_pattern = r'\d{1,5}'  # 숫자만 있는 경우 (1부터 5자리)
    combined_budget_pattern = r'\d+[천백만억조]+'  # 숫자와 한글이 결합된 경우
    korean_budget_pattern = r'[일이삼사오육칠팔구천]+[십만백만천만억조]+원*'  # 한글로 된 숫자 표현

    # 예산 관련 패턴이 포함된 문장을 찾습니다.
    if re.search(r'예산(?:이|은)?', sentence):

        # 숫자와 한글이 결합된 예산을 처리합니다.
        match = re.search(combined_budget_pattern, sentence)
        if match:
            budget_str = match.group()
            numeric_part = re.search(r'\d+', budget_str).group()  # 숫자 부분을 추출합니다.
            korean_part = re.search(r'[천백만억조]+', budget_str)  # 한글 부분을 추출합니다.
            
            if korean_part:
                korean_part = korean_part.group()
                # 숫자를 한글로 변환합니다.
                num_as_kr = num2kr(int(numeric_part), mode=1)
                combined_kr = num_as_kr + korean_part


                # 한글을 숫자로 다시 변환합니다.
                return kr2num(combined_kr)
            else:
                return int(numeric_part)

        # 숫자만 있는 예산을 처리합니다.
        match = re.search(numeric_budget_pattern, sentence)
        if match:
            return int(match.group())

        # 한글만 있는 예산을 처리합니다.
        match = re.search(korean_budget_pattern, sentence)
        if match:
            korean_budget = match.group()
            return kr2num(korean_budget)

    return "None"

def split_text(text):

    number_words = [
    "열", "스물", "서른", "마흔", "쉰", "예순", "일흔", "여든", "아흔",
    "한", "두", "세", "네", "다섯", "여섯", "일곱", "여덟", "아홉"
    ]
    
    # 음절 단위로 텍스트를 분리하기 위해 정규 표현식 패턴 생성합니다.
    pattern = '|'.join(re.escape(word) for word in number_words)
    
    # 텍스트를 정규 표현식 패턴에 따라서 나눕니다.
    split_result = re.findall(pattern, text)
    
    return split_result

# age
def extract_age(sentence):
    numeric_age_pattern = r'\d{1,2}살'  # 숫자+살 패턴
    korean_age_pattern = r'[열스물서른마흔쉰예순일흔여든아흔한두세네다섯여섯일곱여덟아홉]+살'  # 한글 나이 표현 패턴

    # 숫자+살 패턴을 적용합니다.
    match = re.search(numeric_age_pattern, sentence)
    if match:
        age = match.group()
        return int(age.replace('살', ''))

    # 숫자+살 패턴에 매칭되지 않으면 한글 패턴을 적용합니다.
    match = re.search(korean_age_pattern, sentence)
    if match:
        korean_age = match.group().replace('살', '')
        # 한글 나이를 쪼개고 숫자로 변환합니다.
        split_korean_age = split_text(korean_age)
        total_age = sum(kr2num(word) for word in split_korean_age)
        return total_age

    return "None"

# region
def extract_city(text):
    pattern = r'.*(서울|부산|대구|인천|광주|대전|울산|세종|제주).*'
    
    # 패턴과 매칭합니다.
    match = re.match(pattern, text)
    
    # 매칭된 경우 도시 이름 반환, 없으면 None을 반환합니다.
    if match:
        return match.group(1)
    else:
        return "None"