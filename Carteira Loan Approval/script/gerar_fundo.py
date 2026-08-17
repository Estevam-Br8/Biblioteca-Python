import numpy as np
from PIL import Image
from pathlib import Path

print("=" * 50)
print("Gerando Efeito 'Fluxo Contínuo' (Ondas Longitudinais)...")
print("=" * 50)

width, height = 800, 450
frames = 60

# 1. Cores
# Fundo original (#F3F4F6 - Cinza Executivo)
c_base = np.array([243, 244, 246], dtype=float) 
# Cor da onda fluida (um tom suavemente mais escuro para contraste #E5E7EB)
c_onda = np.array([229, 231, 235], dtype=float) 

# 2. Coordenadas da Tela
x = np.linspace(0, 10, width)
y = np.linspace(0, 5.625, height) # Mantendo proporção 16:9
X, Y = np.meshgrid(x, y)

images = []
for i in range(frames):
    # Fase dita a velocidade e o ciclo do loop
    fase = (i / frames) * 2 * np.pi
    
    # 3. Matemática do Fluxo
    # Subtrair o Y do X faz a onda ficar inclinada (diagonal)
    onda = (np.sin(X - Y * 0.5 - fase) + 1) / 2
    
    # Elevar a 1.5 deixa a transição da onda ainda mais esfumaçada e suave
    onda = onda ** 1.5 
    
    onda_exp = onda[..., np.newaxis]
    
    # Mescla
    frame_data = c_base * (1 - onda_exp) + c_onda * onda_exp
    frame_data = np.clip(frame_data, 0, 255).astype(np.uint8)
    
    images.append(Image.fromarray(frame_data))

# Salvamento na subpasta dashboard
pasta_destino = Path(__file__).resolve().parent.parent / "dashboard" / "fundo animado"
pasta_destino.mkdir(parents=True, exist_ok=True)
caminho_saida = pasta_destino / "fundo_fluxo.gif"

images[0].save(
    caminho_saida,
    save_all=True,
    append_images=images[1:],
    duration=60, # Velocidade da animação (60ms)
    loop=0       
)

print(f"[OK] Fundo 'Fluxo Contínuo' salvo em:\n{caminho_saida}")