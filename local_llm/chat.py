from llama_cpp import Llama

llm = Llama(model_path = 'Llama-2-ko-7b-ggml-q4_0.bin',
            n_ctx=1024,
            # n_gpu_layers=1 #gpu 가속을 원하는 경우 주석을 해제하고 Metal(Apple M1) 은 1, Cuda(Nvidia) 는 Video RAM Size 를 고려하여 적정한 수치를 입력합니다.)
      )

output = llm("Q: 인생에 대해서 설명하시오. A: ", max_tokens=1024, stop=["Q:", "\n"], echo=True)

print( output['choices'][0]['text'].replace('▁',' ') )