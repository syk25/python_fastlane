""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

import hlab_parlai_wrapper

# You can choose a model from https://www.parl.ai/docs/zoo.html#model-zoo

# mychatbot = hlab_parlai_wrapper.MyChatbot(model_file = "zoo:wikipedia_full/tfidf_retriever/model") # 위키피디아 암기
# mychatbot = hlab_parlai_wrapper.MyChatbot(model_file = "zoo:dodecadialogue/empathetic_dialogues_ft/model") # 단순
# mychatbot = hlab_parlai_wrapper.MyChatbot(
#     model_file="zoo:blender/blender_400Mdistill/model"  # 3.71G
# )
# mychatbot = hlab_parlai_wrapper.MyChatbot(
#     model_file="zoo:blender/blender_9B/model"  # https://www.parl.ai/docs/zoo.html#blender-9-4b 모델 용량 17.3G
# )

mychatbot = hlab_parlai_wrapper.MyChatbot(model_file="zoo:blender/blender_90M/model")

while True:

    user_input = input("You: ")

    ai_answer = mychatbot.talk_to_ai(user_input)

    print("AI:", ai_answer)
