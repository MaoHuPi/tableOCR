IMAGE_PATH = './image/004e4608.png'
OUTPUT_FILE_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' # 輸出檔案之格式

import cv2
import numpy as np
import pandas as pd
import pytesseract

mimetypeSettingsData = {
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': {
        'function': 'to_excel', 
        'fileExtension': '.xlsx'
    }, 
    'application/vnd.ms-excel': {
        'function': 'to_excel', 
        'fileExtension': '.xls'
    }, 
    'text/csv': {
        'function': 'to_csv', 
        'fileExtension': '.csv'
    }
}

img = cv2.imread(IMAGE_PATH)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img_proxy = cv2.resize(img, (int(100/len(img)*len(img[0])), int(100)), interpolation=cv2.INTER_AREA)
img_proxy = np.copy(img)
img_block = np.copy(img_proxy)
#############################
# 法一：以對角線算長寬，並回推 #
#############################
# def distance(p1, p2):
#     d = False
#     dimension = len(p1)
#     for i in range(dimension):
#         lastD = abs(p1[i] - p2[i])
#         d = math.sqrt(math.pow(d, 2) + math.pow(lastD, 2)) if type(d) != bool else lastD
#     return(d)

# blackPoints = []
# for r_i in range(img_proxy):
#     for c_i in range(img_proxy[r_i]):
#         if img_proxy[r_i, c_i] > 255/2:
#             blackPoints.append([r_i, c_i])

# r_total = 0
# c_total = 0
# centerPoint = False
# for point in blackPoints:
#     r_total += point[0]
#     c_total += point[1]
# r_total /= len(point)
# c_total /= len(point)
# centerPoint = [r_total, c_total]

# maxDistance = 0
# cornerPoint = False
# for point in blackPoints:
#     dist = distance(centerPoint, point)
#     if dist > maxDistance:
#         maxDistance = dist
#         cornerPoint = [*point]
    
# centerPoint
# cornerPoint
# maxDistance

###################################
# 法二：以相關係數得知圖水平軸後旋轉 #
###################################

#################
# 法三：雙軸映射 #
#################
def removeHeadAndTail(l, item):
    l = l[l.index(item):]
    l.reverse()
    l = l[l.index(item):]
    l.reverse()
    return(l)

def countItem(l, item):
    counter = 0
    for i in l:
        if i == item:
            counter += 1
    return(counter)

def dualAxisMapping(img):
    yAxis = [0 for _ in range(len(img))]
    xAxis = [0 for _ in range(len(img[0]))]
    for r_i in range(len(yAxis)):
        for c_i in range(len(xAxis)):
            if img[r_i, c_i] < 255/2:
                yAxis[r_i] = 1
                xAxis[c_i] = 1
    return([xAxis, yAxis])

def mergeSame(axis):
    lastValue = 0
    continuous = [0]
    for v in axis:
        if v != lastValue:
            lastValue = v
            continuous.append(0)
        continuous[-1] += 1
    return(continuous)

def mapping2table(xAxis, yAxis):
    yContinuous = mergeSame(yAxis)
    xContinuous = mergeSame(xAxis)
    if yAxis[0] != 0: yContinuous.insert(0, 0)
    if yAxis[-1] != 0: yContinuous.append(0)
    if xAxis[0] != 0: xContinuous.insert(0, 0)
    if xAxis[-1] != 0: xContinuous.append(0)

    hGaps = xContinuous[::2]
    hGapAverage = sum(xContinuous[::2]) / len(xContinuous[::2])
    minHGap = min(hGaps)
    average = (hGapAverage+minHGap) / 2
    # print(average)
    i = 0
    while i < len(xContinuous):
        if i % 2 == 0:
            hGap = xContinuous[i]
            if hGap < average and i-1 >= 0 and i+1 < len(xContinuous):
                xContinuous[i-1] += xContinuous[i] + xContinuous[i+1]
                xContinuous.pop(i+1)
                xContinuous.pop(i)
                i -= 1
        i += 1

    table = []
    p = 2
    for r_i in range(int((len(yContinuous)-1)/2)):
        table.append([])
        for c_i in range(int((len(xContinuous)-1)/2)):
            table[-1].append([
                sum(yContinuous[:r_i*2-1 + p]), 
                sum(xContinuous[:c_i*2-1 + p]), 
                sum(yContinuous[:r_i*2 + p]), 
                sum(xContinuous[:c_i*2 + p])
            ])
    return(table)

# from ocr.train import modelMethod as ocrModelMethod
import ddddocr
ddddOcr = ddddocr.DdddOcr()
def ocr(img):
    padding = 50
    imgShape = img.shape
    img2 = np.zeros((imgShape[0] + padding*2, imgShape[1] + padding*2), np.uint8)
    img2[padding:padding+imgShape[0], padding:padding+imgShape[1]] = 255 - img[:, :]
    img = img2
    # cv2.imshow('img_ocr', img)
    # cv2.waitKey(-1)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img = Image.fromarray(img)
    return(pytesseract.image_to_string(img))

    # xAxis = dualAxisMapping(img)[0]
    # xContinuous = mergeSame(xAxis)
    # if xAxis[0] != 0:
    #     xContinuous.insert(0, 0)
    # if xAxis[-1] != 0:
    #     xContinuous.append(0)
    # row = []
    # p = 2
    # for c_i in range(int((len(xContinuous)+1)/2)):
    #     row.append([
    #         0, 
    #         sum(xContinuous[:c_i*2-1 + p]), 
    #         len(img)-1, 
    #         sum(xContinuous[:c_i*2 + p])
    #     ])
    # text = ''
    # for rect in row:
    #     img_cell = img[rect[0]:rect[2], rect[1]:rect[3]]
    #     if not(0 in [*img_cell.shape]):
    #         text += ocrModelMethod['predict'](img_cell)[0]
    # return(text)
    
    # padding = 50
    # imgShape = img.shape
    # img2 = np.zeros((imgShape[0] + padding*2, imgShape[1] + padding*2), np.uint8)
    # img2[padding:padding+imgShape[0], padding:padding+imgShape[1]] = 255 - img[:, :]
    # img = img2
    # img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
    # res = ddddOcr.classification(img_bytes)
    # print(res)
    # return(res)

mappingData = dualAxisMapping(img_proxy)
for i in range(len(mappingData)):
    data = mappingData[i]
    data = removeHeadAndTail(data, 0)
    whiteRatio = countItem(data, 0) / len(data)
    mappingData[i] = whiteRatio
# print(mappingData)
mappingData = dualAxisMapping(img_proxy)
# cv2.imshow('img_proxy', img_proxy)
img_block[:, :] = 255
table = mapping2table(*mappingData)
pytesseract.pytesseract.tesseract_cmd = './Tesseract-OCR/tesseract.exe'
from PIL import Image
valueTable = [[0 for c_i in range(len(table[0]))] for r_i in range(len(table))]
for r_i in range(len(table)):
    for c_i in range(len(table[0])):
        rect = table[r_i][c_i]
        img_cell = img_proxy[rect[0]:rect[2], rect[1]:rect[3]]
        if 0 in list(img_cell.shape):
            continue
        ocrRes = ocr(img_cell)
        # print(ocrRes)
        valueTable[r_i][c_i] = ocrRes
        img_block[rect[0]:rect[2], rect[1]:rect[3]] = 0
# cv2.imshow('img_block', img_block)
# cv2.waitKey(-1)
# print(table)

def saveOutputFile(dataList, filePath):
    if filePath[-4:] in ['.png', '.jpg']:
        filePath = filePath[:-4]
    df = pd.DataFrame(data=dataList)
    outputSettings = mimetypeSettingsData[OUTPUT_FILE_MIMETYPE]
    filePath = filePath + outputSettings['fileExtension']
    getattr(df, outputSettings['function'])(filePath)
    print('OUTPUT_PATH: ' + filePath)
    print('')

saveOutputFile(valueTable, IMAGE_PATH)