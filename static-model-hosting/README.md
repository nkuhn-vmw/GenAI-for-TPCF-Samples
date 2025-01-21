
#run these commmands in your local diretory to download the GGUFs from HuggingFace
#mix and match as you see fit

#Please note to host the modle files directoy via a CF app - it must be under 5gb in size.

#chat model runs on cpu-large worker
wget https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q6_K_L.gguf


#embedding model runs on cpu worker
wget https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.f32.gguf


#model url example chat for opsman

#model name:
gemma2:2b

#model url:
https://admin:admin@model-repo.apps.sdc.tpcf.tmm-labs.com/gemma-2-2b-it-Q6_K_L.gguf

#shasum:
b2ef9f67b38c6e246e593cdb9739e34043d84549755a1057d402563a78ff2254



#model name:
nomic-embed-text

#model url:
https://admin:admin@model-repo.apps.sdc.tpcf.tmm-labs.com/nomic-embed-text-v1.5.f32.gguf

#shasum:
ed3a84b570c5513bfd6bfe0ed4cdc8d5a5de5c6b5029fbbc2822d59fc893c1f8
