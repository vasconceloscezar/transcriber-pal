import os
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")


def count_used_tokens(response):
    usage = response["usage"]
    total_tokens = usage["total_tokens"]
    # 🟡 Used tokens this round: Prompt: 10638 tokens, Completion: 295 tokens - 0.12687 USD)
    return (
        f"🟡 Used tokens this round: {total_tokens} "
        # + f"Prompt: {total_tokens} tokens, "
        # + f"Completion: {total_tokens} tokens"
    )


with open("input.txt", "r", encoding="utf-8") as file:
    text = file.read()

openai.api_key = OPENAI_API_KEY

TASK = """
Por favor, analise a seguinte transcrição de áudio de uma reunião e extraia as seguintes informações:

1. Itens acionáveis:
    1. Itens da agenda
    2. Tarefas e delegações
    3. Reuniões e ligações de acompanhamento
    4. Prazos finais

2. Instruções Diretas: Identifique quaisquer gatilhos de ação presentes na transcrição.

3. Tópicos Discutidos: Liste os principais tópicos discutidos durante a reunião.

4. Participantes: Identifique os participantes e analise o estilo de fala e as palavras usadas por eles. Separe por assuntos (assunto1, assunto2,…).

5. Decisões Tomadas: Registre todas as decisões tomadas durante a reunião.

6. Pontos Principais: Destaque os pontos principais e principais ideias de cada tópico.

7. Perguntas e Respostas: Documente quaisquer perguntas feitas e as respostas dadas.

8. Problemas e Soluções: Identifique qualquer problema levantado e as soluções propostas ou implementadas.

9. Dados de Suporte ou Evidências: Identifique quaisquer dados ou evidências que apoiem as decisões tomadas ou os pontos discutidos. Indique também qualquer ligação que possa estar faltando.

10. Emoções: Descreva as emoções exibidas pelos participantes durante a reunião.

11. Consenso e Desacordos: Indique se houve consenso ou desacordos em relação às decisões ou tópicos.

12. Contexto da Reunião: Forneça quaisquer informações contextuais disponíveis que possam ajudar a moldar a análise.

13. Análise Sentimental: Faça uma análise do sentimento geral em relação a certos tópicos ou decisões tomadas.

14. Linguagem Figurativa: Identifique e interprete quaisquer frases idiomáticas, metáforas ou outras formas de linguagem figurativa.

15. Eficácia da Reunião: Avalie quão efetivamente o tempo foi usado e o quanto do conteúdo da agenda foi coberto.

16. Aspectos Culturais: Identifique e compreenda quaisquer nuances culturais que possam influenciar a interpretação do texto.
"""

PROMPT = f"Given the following transcription:  [{text}] \n {TASK}"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": PROMPT},
    ],
)


summary = response["choices"][0]["message"]["content"].strip()


# Save the summary into another TXT file
with open("openai_summary.txt", "w", encoding="utf-8") as file:
    file.write(summary)

print(count_used_tokens(response))
