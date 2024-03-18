from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

# 检查命令行参数
if len(sys.argv) != 3:
    print("Usage: python whpj.py <YYYYMMDD> <CurrencyCode>")
    sys.exit(1)

date = sys.argv[1]
currency_code = sys.argv[2]

currency_code_to_name = {
    "GBP": "英镑",
    "HKD": "港币",
    "USD": "美元",
    "CHF": "瑞士法郎",
    "SGD": "新加坡元",
    "SEK": "瑞典克朗",
    "DKK": "丹麦克朗",
    "NOK": "挪威克朗",
    "JPY": "日元",
    "CAD": "加拿大元",
    "AUD": "澳大利亚元",
    "EUR": "欧元",
    "MOP": "澳门元",
    "PHP": "菲律宾比索",
    "THB": "泰国铢",
    "NZD": "新西兰元",
    "KRW": "韩元",
    "RUB": "卢布",
    "MYR": "林吉特",
    "TWD": "新台币",
    "ESP": "西班牙比塞塔",  
    "ITL": "意大利里拉",  
    "NLG": "荷兰盾",  
    "BEF": "比利时法郎",  
    "FIM": "芬兰马克",  
    "INR": "印度卢比",
    "IDR": "印尼卢比",
    "BRL": "巴西里亚尔",
    "AED": "阿联酋迪拉姆",
    "ZAR": "南非兰特",
    "SAR": "沙特里亚尔",
    "TRY": "土耳其里拉",
}

currency_name = currency_code_to_name.get(currency_code, "未知货币")

# 初始化Safari WebDriver
driver = webdriver.Safari()

try:
    driver.get("https://www.boc.cn/sourcedb/whpj/")

    # 等待页面加载
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pjname")))

    # 选择货币代码
    currency_select = driver.find_element(By.ID, "pjname")
    for option in currency_select.find_elements(By.TAG_NAME, 'option'):
        if option.text == currency_name:
            option.click()
            break

    # 输入日期并搜索
    start_date_input = driver.find_element(By.ID, "erectDate")
    start_date_input.send_keys(date)
    
    end_date_input = driver.find_element(By.ID, "nothing")
    end_date_input.send_keys(date)

    search_button = driver.find_element(By.XPATH, "//input[@class='search_btn' and @onclick='executeSearch()']")
    driver.execute_script("arguments[0].click();", search_button)

    # 等待结果表格出现
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "BOC_main.publish"))
    )

    # 获取现汇卖出价
    # 定位到表格
    rates_table = driver.find_element(By.CLASS_NAME, "BOC_main.publish")
    rows = rates_table.find_elements(By.TAG_NAME, "tr")

    sell_price = None

    # 遍历表格行，寻找匹配的货币并提取现汇卖出价
    for row in rows:
        # 获取每一行的所有列
        cols = row.find_elements(By.TAG_NAME, "td")
        if cols and currency_name in cols[0].text:
            sell_price = cols[3].text  # 现汇卖出价是第四列
            break

    # 将结果打印到文件
    data = str(date)+ " " + currency_code + " " + sell_price
    with open("result.txt", "a") as file:
        file.write(data.strip() + "\n")

    print(sell_price)

except Exception as e:
    # 异常处理
    print("Error:", e)
finally:
    driver.quit()