from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

NUM_SENTENCE = 5


def summarize(long_text, num_sentences=NUM_SENTENCE):
    # Object of automatic summarization.
    auto_abstractor = AutoAbstractor()
    # Set tokenizer.
    auto_abstractor.tokenizable_doc = SimpleTokenizer()
    # Set delimiter for making a list of sentence.
    auto_abstractor.delimiter_list = ["?", "!", ".", "\n"]
    # Object of abstracting and filtering document.
    abstractable_doc = TopNRankAbstractor()
    abstractable_doc.set_top_n(num_sentences)
    # Summarize document.
    result_dict = auto_abstractor.summarize(long_text, abstractable_doc)
    # Output result.
    res = "".join(result_dict["summarize_result"])
    return res

