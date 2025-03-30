

def expand(prompt):

    # 正向提示词
    # 1. 商品信息：描述商品的名称、类型、材质等关键特征;
    # 2. 设定场景：根据商品的特点和目标受众，选择合适的场景;
    # 3、营造氛围：描述光线、色彩、天气等元素来营造氛围;
    # 4、图片风格：可以是写实、卡通、复古、现代简约等风格;
    # 5、画质品质：使用高分辨率、清晰细节、鲜艳色彩等词汇来提升画质;
    # 6、人物角色：商品推广图中需要有人物，要描述人物的外貌、服装、动作、表情等;
    # 反向提示词
    # 1、排除无关元素：避免生成与商品推广无关的元素;
    # 2、杜绝不良效果：防止出现低质量、模糊、变形等问题;
    # 3、规避不适当内容：确保生成的图片不包含不适当或不符合品牌形象的内容，如不含成人内容。
    re_prompt = '''
        撰写图生图的提示词，商品图片以及商品信息已经给出，商品信息：%s ,请按如下模版输出提示词，重要，重要，重要，最后输出的只有英文提示词，模版结构如下
        正向提示词
        1. 商品信息：描述商品的名称、类型、材质等关键特征;
        2. 设定场景：根据商品的特点和目标受众，选择合适的场景;
        3、营造氛围：描述光线、色彩、天气等元素来营造氛围;
        4、图片风格：可以是写实、卡通、复古、现代简约等风格;
        5、画质品质：使用高分辨率、清晰细节、鲜艳色彩等词汇来提升画质;
        6、人物角色：商品推广图中需要有人物，要描述人物的外貌、服装、动作、表情等;
    ''' %(prompt)

    negative_prompt = '''
            Exclude irrelevant elements: Avoid generating elements unrelated to product promotion.
            Eliminate undesirable effects: Prevent low-quality, blurry, distorted, or other subpar outcomes.
            Avoid inappropriate content: Ensure generated images do not contain inappropriate or brand-mismatched content (e.g., no adult content).
       '''
    return re_prompt, negative_prompt