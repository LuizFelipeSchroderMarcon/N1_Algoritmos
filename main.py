import time
import logging
from datadog import initialize, statsd
from utils.data_loader import carregar_dados
from sorts import bubble_sort, merge_sort, quick_sort
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader

initialize(statsd_host='127.0.0.1', statsd_port=8125)

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

spanProcessor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(spanProcessor)

exporter = ConsoleMetricExporter()
reader = PeriodicExportingMetricReader(exporter)

provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter(__name__)

# métricas
execution_time_histogram = meter.create_histogram(
    name="execution_time",
    description="Tempo de execução do algoritmo",
    unit="s"
)

comparisons_counter = meter.create_counter(
    name="comparisons",
    description="Quantidade de comparações"
)

swaps_counter = meter.create_counter(
    name="swaps",
    description="Quantidade de trocas"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def executar_algoritmo(nome_algoritmo, funcao_ordenacao, lista):

    with tracer.start_as_current_span(nome_algoritmo) as span:

        logging.info(f"Início | algoritmo={nome_algoritmo} | tamanho={len(lista)}")

        inicio = time.time()
        lista_ordenada, comp, troc = funcao_ordenacao(lista)
        fim = time.time()

        duracao = fim - inicio

        execution_time_histogram.record(
            duracao,
            {"algorithm": nome_algoritmo, "n": len(lista)}
        )

        comparisons_counter.add(
            comp,
            {"algorithm": nome_algoritmo, "n": len(lista)}
        )

        swaps_counter.add(
            troc,
            {"algorithm": nome_algoritmo, "n": len(lista)}
        )

        # OpenTelemetry 
        span.set_attribute("algoritmo", nome_algoritmo)
        span.set_attribute("tamanho", len(lista))
        span.set_attribute("duracao", duracao)
        span.set_attribute("comparacoes", comp)
        span.set_attribute("trocas", troc)

        # DataDog
        statsd.gauge(
            "algoritmo.tempo_execucao",
            duracao,
            tags=[f"algoritmo:{nome_algoritmo}", f"tamanho:{len(lista)}"]
        )

        statsd.increment(
            "algoritmo.comparacoes",
            comp,
            tags=[f"algoritmo:{nome_algoritmo}"]
        )

        statsd.increment(
            "algoritmo.trocas",
            troc,
            tags=[f"algoritmo:{nome_algoritmo}"]
        )

        logging.info(
            f"Fim | algoritmo={nome_algoritmo} | tamanho={len(lista)} | "
            f"tempo={duracao:.6f}s | comparacoes={comp} | trocas={troc}"
        )

        return {
            "algoritmo": nome_algoritmo,
            "tamanho_base": len(lista),
            "tempo_execucao": duracao,
            "comparacoes": comp,
            "trocas": troc
        }

#
def main():

    algoritmos = [
        ("Bubblesort", bubble_sort.sort),
        ("Mergesort", merge_sort.sort),
        ("Quicksort", quick_sort.sort)
    ]

    tamanhos = [50000]

    resultados_finais = []

    for tamanho in tamanhos:
        logging.info(f"Carregando dados | tamanho={tamanho}")

        caminho_arquivo = f"data/dados_{tamanho}.json"
        lista_original = carregar_dados(caminho_arquivo)

        print(f"\n============= Tamanho base: {tamanho} registros ===========")

        for nome_algoritmo, metodo in algoritmos:
            lista = lista_original.copy()

            resultado = executar_algoritmo(nome_algoritmo, metodo, lista)
            resultados_finais.append(resultado)

            print(
                f"{nome_algoritmo} -> "
                f"tempo: {resultado['tempo_execucao']:.6f}s | "
                f"comparações: {resultado['comparacoes']} | "
                f"trocas: {resultado['trocas']}"
            )

    return resultados_finais


if __name__ == "__main__":
    main()