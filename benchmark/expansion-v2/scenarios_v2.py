"""Fresh bilingual fixtures, authored before v2 inference. Tuples: EN, PT-BR, gold.
Gold follows the translated rubric; records are fictional and contain no real secrets.
"""
TRACKS = {}

def track(name, en, pt, labels, examples, cases):
    assert len(cases) == 12
    TRACKS[name] = dict(instructions={'en': en, 'pt-BR': pt}, labels=labels, examples=examples, cases=cases)

track('sentiment',
 'Classify the writer’s evaluation of the product or service. Positive: praise only. Negative: criticism only. Mixed: both praise and criticism. Neutral: no expressed evaluation. Evaluate the writer, not quoted opinions or hypothetical situations; a factual inconvenience alone is not an evaluation.',
 'Classifique a avaliação do autor sobre o produto ou serviço. Positiva: só elogios. Negativa: só críticas. Mista: elogios e críticas. Neutra: nenhuma avaliação expressa. Considere o autor, não opiniões citadas nem situações hipotéticas; um inconveniente factual, por si só, não é uma avaliação.',
 [('positive','Praise without criticism.','Elogios sem críticas.'),('negative','Criticism without praise.','Críticas sem elogios.'),('mixed','Both praise and criticism.','Elogios e críticas.'),('neutral','No expressed evaluation.','Nenhuma avaliação expressa.')],
 [('A delightful keyboard.','Um teclado excelente.','positive'),('A dreadful screen.','Uma tela péssima.','negative'),('Lovely design, terrible sound.','Design lindo, som péssimo.','mixed'),('The cable is two meters long.','O cabo tem dois metros de comprimento.','neutral')], [
 ('People called it useless. I disagree: it is excellent.','Disseram que era inútil. Discordo: é excelente.','positive'),
 ('I expected a disaster; instead, everything was delightful.','Eu esperava um desastre; em vez disso, tudo foi maravilhoso.','positive'),
 ('Not disappointing at all: the controls are superb.','Não decepcionou nem um pouco: os controles são excelentes.','positive'),
 ('The brochure says “wonderful”; my experience was awful.','O folheto diz “maravilhoso”; minha experiência foi péssima.','negative'),
 ('Great, another crash. What a terrible application.','Ótimo, mais uma falha. Que aplicativo horrível.','negative'),
 ('I would praise it if it worked. As delivered, it is dreadful.','Eu elogiaria se funcionasse. Do jeito que veio, é péssimo.','negative'),
 ('The screen is beautiful, but the battery is dreadful.','A tela é linda, mas a bateria é péssima.','mixed'),
 ('Unlike the awful setup, the daily experience is excellent.','Ao contrário da instalação péssima, o uso diário é excelente.','mixed'),
 ('I love the speed. I still hate its confusing menus.','Adoro a velocidade. Ainda detesto os menus confusos.','mixed'),
 ('The order arrived on Tuesday, two days after the estimate.','O pedido chegou na terça-feira, dois dias depois da previsão.','neutral'),
 ('The survey asks whether the app is wonderful or terrible. I have not answered.','A pesquisa pergunta se o aplicativo é maravilhoso ou péssimo. Ainda não respondi.','neutral'),
 ('If the screen fails, I will be unhappy. I have not tried it yet.','Se a tela falhar, vou ficar insatisfeito. Ainda não testei.','neutral')])

track('intent',
 'Identify the current requested action. Refund means return money; access means restore login; cancel means end a subscription without asking for money back. Other includes a different request, no discernible request, or equally requested actions from multiple categories. Past requests that are explicitly withdrawn do not count.',
 'Identifique a ação solicitada agora. Reembolso significa devolver dinheiro; acesso significa restaurar o login; cancelamento significa encerrar uma assinatura sem pedir devolução de dinheiro. Outro inclui pedido diferente, ausência de pedido identificável ou ações igualmente solicitadas de várias categorias. Pedidos anteriores explicitamente retirados não contam.',
 [('refund','Return money.','Devolver dinheiro.'),('access','Restore login.','Restaurar o login.'),('cancel','End subscription without refund.','Encerrar assinatura sem reembolso.'),('other','Other, missing, or equally competing requests.','Outro, ausente ou pedidos igualmente concorrentes.')],
 [('Please return the payment for my unused voucher.','Devolva o pagamento do meu vale não utilizado.','refund'),('Reset my login so I can enter.','Redefina meu login para eu entrar.','access'),('Stop renewing my subscription; keep the payment.','Pare de renovar minha assinatura; pode ficar com o pagamento.','cancel'),('Please change my delivery address.','Altere meu endereço de entrega.','other')], [
 ('Keep my subscription active; just reverse the extra payment.','Mantenha minha assinatura ativa; só estorne o pagamento extra.','refund'),
 ('I can log in now. The remaining request is to return yesterday’s charge.','Já consigo entrar. O pedido que falta é devolver a cobrança de ontem.','refund'),
 ('I am not asking to cancel; I need my money back for that duplicate transaction.','Não estou pedindo cancelamento; preciso da devolução daquela transação duplicada.','refund'),
 ('Do not refund or cancel anything. Help me get into my account.','Não reembolse nem cancele nada. Me ajude a entrar na minha conta.','access'),
 ('My invoice is paid, but authentication rejects me. Restore my login.','Minha fatura está paga, mas a autenticação me rejeita. Restaure meu login.','access'),
 ('Ignore my earlier cancellation request. I only want to recover access.','Desconsidere meu pedido anterior de cancelamento. Só quero recuperar o acesso.','access'),
 ('I can still log in. End the plan before its next renewal; no refund needed.','Ainda consigo entrar. Encerre o plano antes da próxima renovação; não preciso de reembolso.','cancel'),
 ('Do not return the money. I only want the subscription closed.','Não devolva o dinheiro. Só quero encerrar a assinatura.','cancel'),
 ('I previously wanted a refund; withdraw that request and stop the plan instead.','Antes eu queria reembolso; retiro esse pedido e peço o encerramento do plano.','cancel'),
 ('Please both restore access and refund the charge. Neither request has priority.','Restaure o acesso e reembolse a cobrança. Nenhum dos pedidos tem prioridade.','other'),
 ('What happens to stored files if I cancel someday? I am not requesting cancellation.','O que acontece com os arquivos se eu cancelar algum dia? Não estou pedindo cancelamento.','other'),
 ('My login screen mentions refunds and cancellations. That is all I wanted to report.','Minha tela de login menciona reembolsos e cancelamentos. Era só isso que eu queria relatar.','other')])

track('entailment',
 'Using only the premise, judge the claim. Supported means necessarily true; contradicted means necessarily false; unknown means neither follows. Do not assume unstated facts. “Some” means at least one, not necessarily all. “Only X can Y” means Y requires X, not that every X does Y.',
 'Usando apenas a premissa, julgue a afirmação. Sustentada significa necessariamente verdadeira; contradita significa necessariamente falsa; indeterminada significa que nenhuma das duas conclusões decorre da premissa. Não suponha fatos não informados. “Alguns” significa pelo menos um, não necessariamente todos. “Só X pode Y” significa que Y exige X, não que todo X faça Y.',
 [('supported','Claim necessarily follows.','A afirmação decorre necessariamente.'),('contradicted','The opposite necessarily follows.','O contrário decorre necessariamente.'),('unknown','Neither follows.','Nenhuma das duas conclusões decorre.')],
 [('Premise: All blue cards are valid. This card is blue. Claim: This card is valid.','Premissa: Todos os cartões azuis são válidos. Este cartão é azul. Afirmação: Este cartão é válido.','supported'),('Premise: No window is open. Claim: At least one window is open.','Premissa: Nenhuma janela está aberta. Afirmação: Pelo menos uma janela está aberta.','contradicted'),('Premise: A package arrived. Claim: The package is heavy.','Premissa: Um pacote chegou. Afirmação: O pacote é pesado.','unknown')], [
 ('Premise: Only editors can publish. Rita published. Claim: Rita is an editor.','Premissa: Só editores podem publicar. Rita publicou. Afirmação: Rita é editora.','supported'),
 ('Premise: Some invoices are unpaid. Claim: At least one invoice is unpaid.','Premissa: Algumas faturas não foram pagas. Afirmação: Pelo menos uma fatura não foi paga.','supported'),
 ('Premise: Every failed job is retried. Job K failed. Claim: Job K is retried.','Premissa: Todo processamento que falha é repetido. O processamento K falhou. Afirmação: O processamento K é repetido.','supported'),
 ('Premise: Nilo arrived before Bia, who arrived before Caio. Claim: Nilo arrived before Caio.','Premissa: Nilo chegou antes de Bia, que chegou antes de Caio. Afirmação: Nilo chegou antes de Caio.','supported'),
 ('Premise: No archived record can be edited. Record R is archived. Claim: Record R can be edited.','Premissa: Nenhum registro arquivado pode ser editado. O registro R está arquivado. Afirmação: O registro R pode ser editado.','contradicted'),
 ('Premise: Exactly one server failed. Claim: No server failed.','Premissa: Exatamente um servidor falhou. Afirmação: Nenhum servidor falhou.','contradicted'),
 ('Premise: The launch happened after the review. Claim: The launch happened before the review.','Premissa: O lançamento ocorreu depois da revisão. Afirmação: O lançamento ocorreu antes da revisão.','contradicted'),
 ('Premise: All three named payments were reversed. Claim: One of those three payments was not reversed.','Premissa: Todos os três pagamentos citados foram estornados. Afirmação: Um desses três pagamentos não foi estornado.','contradicted'),
 ('Premise: Only editors can publish. Rita is an editor. Claim: Rita published.','Premissa: Só editores podem publicar. Rita é editora. Afirmação: Rita publicou.','unknown'),
 ('Premise: Every failed job is retried. Job K was retried. Claim: Job K failed.','Premissa: Todo processamento que falha é repetido. O processamento K foi repetido. Afirmação: O processamento K falhou.','unknown'),
 ('Premise: Some invoices are unpaid. Claim: Every invoice is unpaid.','Premissa: Algumas faturas não foram pagas. Afirmação: Todas as faturas não foram pagas.','unknown'),
 ('Premise: The meeting is either Tuesday or Thursday, but not both. Claim: The meeting is Tuesday.','Premissa: A reunião é na terça ou na quinta, mas não nas duas. Afirmação: A reunião é na terça.','unknown')])

track('retrieval',
 'Judge whether the passage answers the question. Full: it explicitly supplies every requested item. Partial: it supplies at least one but not every requested item. None: it supplies no requested item, even if its vocabulary overlaps. Use only the passage, not background knowledge.',
 'Julgue se o trecho responde à pergunta. Completa: informa explicitamente todos os itens pedidos. Parcial: informa pelo menos um, mas não todos. Nenhuma: não informa nenhum item pedido, mesmo com vocabulário parecido. Use apenas o trecho, não conhecimento externo.',
 [('full','All requested items answered.','Todos os itens pedidos são respondidos.'),('partial','Some but not all items answered.','Alguns itens pedidos são respondidos, mas não todos.'),('none','No requested item answered.','Nenhum item pedido é respondido.')],
 [('Question: Where and when is the demo? Passage: Room A, at noon.','Pergunta: Onde e quando será a demonstração? Trecho: Sala A, ao meio-dia.','full'),('Question: Where and when is the demo? Passage: It is at noon.','Pergunta: Onde e quando será a demonstração? Trecho: Será ao meio-dia.','partial'),('Question: Where is the demo? Passage: Demos help explain products.','Pergunta: Onde será a demonstração? Trecho: Demonstrações ajudam a explicar produtos.','none')], [
 ('Question: Can guests export files? Passage: Export is disabled for guest accounts.','Pergunta: Visitantes podem exportar arquivos? Trecho: A exportação está desativada para contas de visitantes.','full'),
 ('Question: Which header carries the key? Passage: Put the key in X-Access-Key; Authorization is not used.','Pergunta: Qual cabeçalho leva a chave? Trecho: Coloque a chave em X-Access-Key; Authorization não é usado.','full'),
 ('Question: What is the limit and what happens above it? Passage: The cap is 40 items; larger requests are rejected.','Pergunta: Qual é o limite e o que acontece acima dele? Trecho: O máximo é 40 itens; pedidos maiores são rejeitados.','full'),
 ('Question: Does expiry delete backups? Passage: Expiry never deletes backups; it only disables sharing.','Pergunta: O vencimento exclui os backups? Trecho: O vencimento nunca exclui os backups; só desativa o compartilhamento.','full'),
 ('Question: What are the price and minimum term? Passage: The service costs 12 credits per month.','Pergunta: Quais são o preço e o prazo mínimo? Trecho: O serviço custa 12 créditos por mês.','partial'),
 ('Question: Which role can restore, and how long does restoration take? Passage: Only owners can restore.','Pergunta: Qual função pode restaurar e quanto tempo demora a restauração? Trecho: Só proprietários podem restaurar.','partial'),
 ('Question: What is the retention period and can it be extended? Passage: Retention lasts 18 days.','Pergunta: Qual é o período de retenção e ele pode ser prorrogado? Trecho: A retenção dura 18 dias.','partial'),
 ('Question: Is encryption enabled and which cipher is used? Passage: Encryption is enabled by default.','Pergunta: A criptografia está ativada e qual cifra é usada? Trecho: A criptografia vem ativada por padrão.','partial'),
 ('Question: What is the retention period? Passage: Retention settings appear in the retention menu.','Pergunta: Qual é o período de retenção? Trecho: As configurações de retenção aparecem no menu de retenção.','none'),
 ('Question: How can I restore a deleted record? Passage: To delete a record, click Remove.','Pergunta: Como restauro um registro excluído? Trecho: Para excluir um registro, clique em Remover.','none'),
 ('Question: Which role is required to approve? Passage: An approval notification is sent to managers.','Pergunta: Qual função é exigida para aprovar? Trecho: Uma notificação de aprovação é enviada aos gerentes.','none'),
 ('Question: What caused the outage? Passage: The outage began at 09:00 and ended at 09:20.','Pergunta: O que causou a indisponibilidade? Trecho: A indisponibilidade começou às 09:00 e terminou às 09:20.','none')])

track('data_handling',
 'Classify the contents under this fictional rule, not law. Credential: a usable login password, recovery code or authentication token is disclosed. Personal: an individual’s email, phone or home address is disclosed, without a credential. Public: neither is disclosed. Mere mentions, redacted placeholders and explicitly revoked credentials do not count. A team’s public contact address is not an individual’s address. Credential has priority.',
 'Classifique o conteúdo segundo esta regra fictícia, não segundo a lei. Credencial: revela uma senha de login, código de recuperação ou token de autenticação utilizável. Pessoal: revela e-mail, telefone ou endereço residencial de uma pessoa, sem credencial. Público: não revela nenhum dos dois. Menções, marcadores censurados e credenciais explicitamente revogadas não contam. Um contato público de equipe não é o endereço de uma pessoa. Credencial tem prioridade.',
 [('credential','Usable authentication secret disclosed.','Segredo de autenticação utilizável revelado.'),('personal','Individual contact data, no usable secret.','Contato de uma pessoa, sem segredo utilizável.'),('public','Neither qualifying category disclosed.','Nenhuma das categorias anteriores é revelada.')],
 [('Fictional example: current login password = DemoKey44.','Exemplo fictício: senha atual de login = DemoKey44.','credential'),('Fictional contact: Marina’s home is at 7 Pine Lane.','Contato fictício: Marina mora na Rua dos Pinheiros, 7.','personal'),('The documentation explains what a password is.','A documentação explica o que é uma senha.','public')], [
 ('Fictional record: The active recovery code is RCV-2846, not the invoice identifier.','Registro fictício: O código de recuperação ativo é RCV-2846, não o identificador da fatura.','credential'),
 ('Fictional record: Lia’s email is lia@example.test and her current login password is Cedar7!.','Registro fictício: O e-mail de Lia é lia@example.test e sua senha atual de login é Cedar7!.','credential'),
 ('Fictional record: Use token DEMO-KEY-731 to authenticate; it has not been revoked.','Registro fictício: Use o token DEMO-KEY-731 para autenticar; ele não foi revogado.','credential'),
 ('Fictional record: Old password was removed. New active password: River92!.','Registro fictício: A senha antiga foi removida. Nova senha ativa: River92!.','credential'),
 ('Fictional record: Personal email: bia@example.test. Password: [REDACTED].','Registro fictício: E-mail pessoal: bia@example.test. Senha: [CENSURADA].','personal'),
 ('Fictional record: Nilo lives at 18 Oak Street. No password is shown.','Registro fictício: Nilo mora na Rua dos Carvalhos, 18. Nenhuma senha é exibida.','personal'),
 ('Fictional record: Revoke token DEMO-99: revocation is now complete. Owner email: caio@example.test.','Registro fictício: Revogue o token DEMO-99: a revogação já foi concluída. E-mail do dono: caio@example.test.','personal'),
 ('Fictional record: Email Joana personally at joana@example.test; the team’s public inbox is separate.','Registro fictício: Escreva para Joana pessoalmente em joana@example.test; a caixa pública da equipe é outra.','personal'),
 ('Fictional record: The invoice ID is PASSWORD-523. It cannot authenticate anyone.','Registro fictício: O ID da fatura é PASSWORD-523. Ele não pode autenticar ninguém.','public'),
 ('Fictional record: Token DEMO-22 was revoked yesterday and cannot be used.','Registro fictício: O token DEMO-22 foi revogado ontem e não pode ser usado.','public'),
 ('Public team contact: support@example.test. No individual contact or credential is supplied.','Contato público da equipe: support@example.test. Nenhum contato individual nem credencial é fornecido.','public'),
 ('The text says “never reveal passwords”; the actual value is [REDACTED].','O texto diz “nunca revele senhas”; o valor real está [CENSURADO].','public')])

track('current_status',
 'Determine the current incident state using the latest timestamped verified observation. Resolved: service is fully working. Ongoing: a service impairment remains. Unknown: no verified observation or conflicting observations at the latest time. Predictions, promises and earlier observations cannot override the latest verified observation.',
 'Determine o estado atual do incidente pela observação verificada de horário mais recente. Resolvido: o serviço funciona totalmente. Em andamento: ainda há prejuízo ao funcionamento. Indeterminado: não há observação verificada ou há observações conflitantes no horário mais recente. Previsões, promessas e observações anteriores não substituem a observação verificada mais recente.',
 [('resolved','Latest verified observation: fully working.','Última observação verificada: funciona totalmente.'),('ongoing','Latest verified observation: impairment remains.','Última observação verificada: ainda há prejuízo.'),('unknown','No decisive latest verified observation.','Sem observação verificada mais recente que seja conclusiva.')],
 [('Verified 08:00: all healthy.','Verificado às 08:00: tudo funciona.','resolved'),('Verified 08:00: login still fails.','Verificado às 08:00: o login ainda falha.','ongoing'),('No monitoring result exists yet.','Ainda não há resultado do monitoramento.','unknown')], [
 ('Verified 10:00: fully restored. Verified 09:00: offline. Display order is not chronological.','Verificado às 10:00: totalmente restaurado. Verificado às 09:00: fora do ar. A ordem de exibição não é cronológica.','resolved'),
 ('Verified 11:00: service fully healthy. A customer guesses it may fail tonight.','Verificado às 11:00: serviço totalmente normal. Um cliente acha que pode falhar à noite.','resolved'),
 ('Verified 09:00: exports fail. Verified 10:00: every function works again.','Verificado às 09:00: as exportações falham. Verificado às 10:00: todas as funções voltaram a funcionar.','resolved'),
 ('Verified 12:00: normal service. An unverified 12:30 complaint says everything is down.','Verificado às 12:00: serviço normal. Uma reclamação não verificada das 12:30 diz que tudo está fora do ar.','resolved'),
 ('Verified 10:00: restored. Verified 11:00: exports stopped again.','Verificado às 10:00: restaurado. Verificado às 11:00: as exportações pararam de novo.','ongoing'),
 ('Verified 14:00: login fails. The vendor promises recovery at 15:00; no later check exists.','Verificado às 14:00: o login falha. O fornecedor promete recuperação às 15:00; não há verificação posterior.','ongoing'),
 ('Verified 15:00: only exports still fail; all other functions recovered.','Verificado às 15:00: só as exportações ainda falham; as outras funções foram recuperadas.','ongoing'),
 ('Verified 16:00: production remains slow. Verified 15:00: everything was normal.','Verificado às 16:00: a produção continua lenta. Verificado às 15:00: tudo estava normal.','ongoing'),
 ('At 10:00 one verified monitor says healthy and another equally authoritative verified monitor says offline.','Às 10:00 um monitor verificado diz normal e outro monitor verificado, de igual autoridade, diz fora do ar.','unknown'),
 ('The vendor says it fixed the issue, but no verified observations exist.','O fornecedor diz que corrigiu o problema, mas não há observações verificadas.','unknown'),
 ('Verified 09:00: healthy. At 10:00 two equally authoritative verified observations conflict: healthy and failed.','Verificado às 09:00: normal. Às 10:00 duas observações verificadas, de igual autoridade, entram em conflito: normal e falhou.','unknown'),
 ('A forecast predicts an outage tomorrow. Current telemetry has never been collected.','Uma previsão aponta queda amanhã. A telemetria atual nunca foi coletada.','unknown')])

track('threshold_policy',
 'Apply the trusted rule stated in the record to the stated verified measurements. Escalate if the rule is established true; monitor if established false; unknown if necessary evidence is missing or the measurement interval crosses the boundary. Use inclusive/exclusive comparisons exactly. Do not infer missing measurements.',
 'Aplique a regra confiável informada no registro às medições verificadas apresentadas. Escalar se a regra for comprovadamente verdadeira; monitorar se for comprovadamente falsa; indeterminado se faltar evidência necessária ou o intervalo de medição cruzar o limite. Respeite exatamente comparações inclusivas e exclusivas. Não deduza medições ausentes.',
 [('escalate','Rule established true.','Regra comprovadamente verdadeira.'),('monitor','Rule established false.','Regra comprovadamente falsa.'),('unknown','Cannot determine truth of rule.','Não é possível determinar se a regra é verdadeira.')],
 [('Rule: escalate at 8 or more failures. Verified: 9 failures.','Regra: escalar com 8 ou mais falhas. Verificado: 9 falhas.','escalate'),('Rule: escalate above 8 failures. Verified: 2 failures.','Regra: escalar acima de 8 falhas. Verificado: 2 falhas.','monitor'),('Rule: escalate above 8 failures. Failure count unavailable.','Regra: escalar acima de 8 falhas. A contagem de falhas não está disponível.','unknown')], [
 ('Rule: escalate at least 3 failures. Verified: exactly 3 failures.','Regra: escalar com pelo menos 3 falhas. Verificado: exatamente 3 falhas.','escalate'),
 ('Rule: escalate above 2% error rate. Verified: error rate 2.1%.','Regra: escalar acima de 2% de erros. Verificado: taxa de erros de 2,1%.','escalate'),
 ('Rule: escalate if delay exceeds 60 seconds. Verified: delay is 2 minutes.','Regra: escalar se o atraso ultrapassar 60 segundos. Verificado: atraso de 2 minutos.','escalate'),
 ('Rule: escalate if failures are at least 10. Verified: failure count lies from 11 to 14 inclusive.','Regra: escalar se houver pelo menos 10 falhas. Verificado: a contagem está entre 11 e 14, inclusive.','escalate'),
 ('Rule: escalate above 3 failures. Verified: exactly 3 failures.','Regra: escalar acima de 3 falhas. Verificado: exatamente 3 falhas.','monitor'),
 ('Rule: escalate above 2% error rate. Verified: error rate exactly 2%.','Regra: escalar acima de 2% de erros. Verificado: taxa de erros de exatamente 2%.','monitor'),
 ('Rule: escalate only if BOTH error rate exceeds 5% AND delay exceeds 30 seconds. Verified: delay 20 seconds; error rate unavailable.','Regra: escalar somente se AMBAS ocorrerem: taxa de erros acima de 5% E atraso acima de 30 segundos. Verificado: atraso de 20 segundos; taxa de erros indisponível.','monitor'),
 ('Rule: escalate at least 10 failures. Verified: count lies from 4 to 9 inclusive.','Regra: escalar com pelo menos 10 falhas. Verificado: a contagem está entre 4 e 9, inclusive.','monitor'),
 ('Rule: escalate above 3 failures. Verified: failure count is either 3 or 4.','Regra: escalar acima de 3 falhas. Verificado: a contagem de falhas é 3 ou 4.','unknown'),
 ('Rule: escalate above 2% error rate. Error rate has not been measured.','Regra: escalar acima de 2% de erros. A taxa de erros não foi medida.','unknown'),
 ('Rule: escalate if ANY of these holds: error rate above 5%, delay above 30 seconds. Verified: delay 20 seconds; error rate unavailable.','Regra: escalar se QUALQUER destas ocorrer: taxa de erros acima de 5%, atraso acima de 30 segundos. Verificado: atraso de 20 segundos; taxa de erros indisponível.','unknown'),
 ('Rule: escalate at least 10 failures. Verified: count lies from 8 to 12 inclusive.','Regra: escalar com pelo menos 10 falhas. Verificado: a contagem está entre 8 e 12, inclusive.','unknown')])
