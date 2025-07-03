import base64
from fpdf import FPDF

def create_sample_paper():
    """Create a sample scientific paper for testing purposes."""
    
    # Sample paper content
    paper_content = """
    Attention Is All You Need: A Novel Architecture for Neural Machine Translation
    
    Abstract
    
    The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show that these models are superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing with large amounts of training data.
    
    Introduction
    
    Recurrent neural networks, long short-term memory and gated recurrent neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems such as language modeling and machine translation. Numerous efforts have since continued to push the boundaries of recurrent language models and encoder-decoder architectures.
    
    Recurrent models typically factor computation along the symbol positions of the input and output sequences. Aligning the positions to steps in computation time, they generate a sequence of hidden states ht, as a function of the previous hidden state ht−1 and the input for position t. This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths, as memory constraints limit batching across examples.
    
    Methods
    
    Most competitive neural sequence transduction models have an encoder-decoder structure. Here, the encoder maps an input sequence of symbol representations (x1, ..., xn) to a sequence of continuous representations z = (z1, ..., zn). Given z, the decoder then generates an output sequence (y1, ..., ym) of symbols one element at a time. At each step the model is auto-regressive, consuming the previously generated symbols as additional input when generating the next.
    
    The Transformer follows this overall architecture using stacked self-attention and point-wise, fully connected layers for both the encoder and decoder, shown in the left and right halves of Figure 1, respectively.
    
    Results
    
    We evaluate the Transformer on English-to-German and English-to-French translation using the WMT 2014 English-German dataset consisting of about 4.5M sentence pairs. Sentences were encoded using byte-pair encoding, which has a shared source-target vocabulary of about 37000 tokens. For English-French, we used the significantly larger WMT 2014 English-French dataset consisting of 36M sentences and split tokens into a 32000 word-piece vocabulary.
    
    Our base models achieved a BLEU score of 27.3 on the English-to-German translation task, which is better than any previously reported single model. The big Transformer model (Transformer (big) in Table 2) outperforms the best previously reported model (including ensembles) by more than 2.0 BLEU, establishing a new state-of-the-art BLEU score of 28.4.
    
    Discussion
    
    While the Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequence-aligned RNNs or convolution, there have been several recent works using self-attention in various contexts. In the following, we discuss how our work relates to these previous approaches.
    
    The Transformer is the first model to use self-attention for transduction, while most previous work with self-attention applies it to tasks with a single input sentence or document, such as reading comprehension, abstractive summarization, textual entailment, or learning task-independent sentence representations.
    
    Conclusion
    
    In this work, we presented the Transformer, the first sequence transduction model based entirely on attention, replacing the recurrent layers most commonly used in encoder-decoder architectures with multi-headed self-attention.
    
    For translation tasks, the Transformer can be trained significantly faster than architectures based on recurrent or convolutional layers. On both WMT 2014 English-to-German and WMT 2014 English-to-French translation tasks, we achieve a new state of the art. In the former task our best model outperforms even all previously reported ensembles.
    
    We are excited about the future of attention-based models and plan to apply them to other tasks. We plan to extend the Transformer to problems involving input and output modalities other than text and to investigate local, restricted attention mechanisms to efficiently handle large inputs and outputs such as images, audio and video. Making generation less sequential is another research goals of ours.
    
    References
    
    1. Bahdanau, D., Cho, K., and Bengio, Y. Neural machine translation by jointly learning to align and translate. arXiv preprint arXiv:1409.0473, 2014.
    2. Gehring, J., Auli, M., Grangier, D., Yarats, D., and Dauphin, Y. N. Convolutional sequence to sequence learning. arXiv preprint arXiv:1705.03122, 2017.
    3. Hochreiter, S. and Schmidhuber, J. Long short-term memory. Neural computation, 9(8):1735–1780, 1997.
    """
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Split content into lines and add to PDF
    lines = paper_content.split('\n')
    for line in lines:
        if line.strip():
            # Clean Unicode characters that might cause issues
            clean_line = line.strip().replace('−', '-').replace('–', '-').replace('—', '-')
            if clean_line.upper() in ['ABSTRACT', 'INTRODUCTION', 'METHODS', 'RESULTS', 'DISCUSSION', 'CONCLUSION', 'REFERENCES']:
                pdf.set_font("Arial", 'B', 14)
                pdf.multi_cell(0, 10, clean_line)
                pdf.set_font("Arial", size=12)
            else:
                pdf.multi_cell(0, 10, clean_line)
        else:
            pdf.multi_cell(0, 5, "")
    
    # Save the PDF
    pdf.output("sample_paper.pdf")
    print("✅ Sample paper created as 'sample_paper.pdf'")
    
    return "sample_paper.pdf"

if __name__ == "__main__":
    create_sample_paper() 