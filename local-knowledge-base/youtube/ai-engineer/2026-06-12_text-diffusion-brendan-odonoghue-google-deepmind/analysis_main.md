# Text Diffusion — Brendan O’Donoghue, Google DeepMind  
**Kanál:** AI Engineer  
**URL:** https://youtu.be/r305-aQTaU0?si=U_CUojaS_HO_Ap9Z

## Úvod

Some people are still filtering into the room, but it's mostly intro stuff for the first couple of slides so they won't miss anything. Okay, welcome everybody.

My name is Brendan. I'm a research scientist at DeepMind. I'm talking today about text diffusion, which is a more forward-looking research area at DeepMind.

You're probably familiar with image and video diffusion, which is state of the art for these modalities right now: you take a ground truth image, add noise to it in training, and then train a neural network to remove that noise gradually. At inference time you initialize the picture with pure noise and iteratively refine it to recover the image, video, audio, or whatever you're looking for.

The principle is essentially the same for text diffusion. You start with a clean sequence of tokens, like a clean sentence, and then gradually add noise and corrupt it somehow. There are lots of different ways to do that. You can do it in a continuous or discrete way, but let's just say discrete for now, which in this case means adding random tokens or replacing tokens with other random tokens. You do that for a bunch of different noise levels, and you train the neural network to fill in and correct the mistakes in the text. Then at inference time you initialize the sequence of tokens to pure noise, like pure random discrete tokens from the vocabulary, and iteratively refine through that to recover a clean sentence.

In practice, if you look at GIFs of this for images, you get a very similar process for text. It starts off noisy and gradually fills in, and you get relatively clean outputs at the end.

The team I'm on had a research demo release about a year ago called Gemini diffusion, which was a variant of a Gemini model that did text diffusion instead of autoregressive next-token generation. It was a research preview open to about 100k people. We still have new developments in that direction coming up soon, so keep posted.

We had some good numbers at the time, though it's a year ago, which is prehistoric in this field. Our main competitor model was Gemini 2.0 Flashlight at the time, because that was the architecture we were branching from, and we basically had very similar quality across the board. We had a little bit of advantage in code, a little bit of disadvantage in some other areas, but relatively similar performance at much better latencies. Again, this is a year ago, so I wouldn't fixate too much on these numbers.

## Autoregressive generation vs. diffusion

What's the difference between autoregressive generation and diffusion?

In standard vanilla Gemini, Gemma, GPT, whatever, generation of text works like this: you have some context coming in and you want to generate a response, and the model does it one token at a time. It generates the first token, then conditions on that to generate the next token, and so on.

Whereas in diffusion, a context comes in, and it initializes a long sequence of tokens — could be hundreds, could be thousands, could be shorter depending on the model — to random noise. Then it iteratively refines that canvas to remove the noise over the course of a few denoising steps. So rather than one token at a time, it does the entire block together, but over a couple of iterations. It's not just one pass; it does multiple passes, but it gets to attend to the future tokens and so on.

So it's a different way of generating text.

That obviously has some pros and cons. The main pro people really like, and probably the biggest advantage that text-to-image models have, is that it's faster inference. It generates more tokens per second because it makes much better use of the hardware, the TPU and the GPU. I have some slides on that to explain why.

Some other advantages are that it can do bidirectional attention within the canvas of tokens. Autoregressive models can only attend to the past; they have causal attention within their transformer. A text-to-image model is not restricted at all. It can attend to the future. That has interesting properties like self-correcting generation based on future tokens. It can do some reasoning, see that it got the answer incorrect, and then go back and fix the reasoning and do it again. I have a demo of that.

Because the process is iterative, it does a number of steps to respond, which means the model can actually do adaptive computation. You can train the model to spend more time on harder problems and less time on easier problems. Like diffusion models in general, you can do things like in-place editing, where you say “fix the last tokens and give me the prefix that corresponds to those tokens” and so on.

The main disadvantage, and the reason it isn't used everywhere right now, is lower throughput for large batches. Autoregressive models are slow, but you can have a big batch of queries together and push that through the neural network on the GPU. Each individual user is slow, but you make good use of the TPU by doing that, so you can serve a lot of queries and keep costs down.

Since text diffusion does multiple forward passes on the same data, it hits a compute threshold earlier. Even though it's lower latency for any one user, it tends to be lower throughput overall, so the cost to serve is higher. Right now, if you've played with Claude recently, you'll know they have throughput concerns. People really care about throughput right now, and that's why no one is landing text diffusion into these big models primarily: it's too expensive to serve, even if it is much lower latency.

## Why latency is lower

Just to explain why it has lower latency, in case you're not familiar with how GPUs and TPUs run today: in a GPU there's a tensor core that does big matrix multiplies. It's very efficient and has a lot of FLOPs. Then there is the memory sitting on the GPU or TPU, HBM, where the weights and activations are stored, and that has to transfer over from memory, including the weights, activations, and KV cache, into the tensor core in order to do the computation.

That flow through the bandwidth channel is tight. Both GPUs and TPUs have a lot of FLOPs and not that much bandwidth. It's expensive to put bandwidth onto these chips, and it's easy to put FLOPs. Because of that ratio, the more FLOPs you do for each stream of data you put through, the better.

When we serve an autoregressive model, these chips are memory bound. They're bottlenecked by this bandwidth. In autoregressive next-token generation, for each token, say batch size one, you have to stream over the entire neural network and all the KV cache to get one token, and then you do it again for the next token and so on.

Whereas for text diffusion, you're generating, say, 256 tokens. You still stream over everything, but if you can do that fewer times than the number of tokens because of this iterative refinement process, then you get a speedup. If you can do, say, 24 passes to generate 256 tokens, you'll be doing 10 times fewer memory transfers than an autoregressive model. If you're truly memory bound, then you'll be about 10 times faster.

That's the real hardware reason why text-to-image models are much lower latency than autoregressive models.

We had the Gemini diffusion demo, and maybe some of you got access to it last year. It was able to hit something like 2,000 tokens a second pretty consistently, depending on the length of the query. Obviously it depends. The longer the sequence it's generating, the less it is prefill dominated, and so you can really lean into these very long sequences of very fast tokens. If you're only generating one token, for instance, you'll be dominated by the cost of the prefill. The tokens-per-second number on the webpage incorporated prefill and everything. Those were genuine raw tokens that you would receive in your web browser.

## Bidirectional reasoning and self-correction

I want to dig into some of the other advantages that text diffusion has, which are a little less talked about in the literature, but I think are pretty cool.

At Google I/O last year, they showed a demo for the text-to-image model. It's a very easy prompt, but lots of models actually make mistakes on it. The prompt is: “What is the square root of 81 * 2/3 squared plus blah blah blah?” I think the answer is 39.

You pass that into the model and ask Gemini diffusion to respond to it. After one forward pass, these are the tokens it's generated. Since it's an iterative refinement process, a one forward pass is not all it's going to do, but after one forward pass it has this: answer equals and then it said 60. It's not correct, but that's what it's guessing for now. Then it starts to do the reasoning: solution calculate square root of 81 and so on.

After two forward passes, it's changed 60 to 49, and it's gotten a little further into the reasoning. It's gotten like five steps into the reasoning, 2 squared equals 4, and some of the blue tokens are still going to change.

After three forward passes, it's gotten all the way through the reasoning. It gets the answer correct at the end: 36 + 3 is equal to 39. And it's gone back and fixed the original response to say 39. It had a mistake twice, 60 and then 49, but once it finished the reasoning, it was able to return and fix the mistake it made at the start.

It will do a couple more forward passes to fix some of these tokens that aren't quite right in the text, but overall that's basically the structure of the output it returns. This is a property that text diffusion models have: the ability to do bidirectional reasoning, to not only see the past but also see the future that it's going to utter, and to use that information to do self-correction.

At the time, much bigger models than the one we were serving made a mistake on this problem. Both ChatGPT-4o, which was new at the time, and Gemini 2.5 Flash, which was brand new at the time, made an error on this exact problem. You give them the exact same prompt, and they would say something like remember the answer is 39. GPT-4o said 40. It went through the reasoning and then said it managed to figure out it was 39 and said, “I made a mistake. It's 39, not 40.” Gemini 2.5 Flash also made a mistake, said 42, and then stuck to its guns and never changed it: “36 + 3 is 42.” It incorporated the error into its reasoning later.

These are much bigger models than the Gemini diffusion models, so this really is a property, or a flaw, of autoregressive models that text diffusion models don't have. You can fix this with modern reasoning and thinking models, but then you're just punting the problem elsewhere.

## Dynamic and adaptive computation

Another advantage is dynamic computation. You can give the model more time at inference, more forward passes, a bigger budget, and it can do better. It's not exactly monotonic, but it is roughly monotonic that quality across every eval basically continues to go up because it gets to look at the nearly clean and correct solution and then fix the mistake. So you get this nice curve where as the number of denoising steps, or forward passes, increases, the quality overall gets higher.

These are just six coding evals that we monitor internally.

A slightly different concept is adaptive computation, which means you can train the model in a way that lets it determine itself when it is finished. Then for easy responses it can use a little bit of compute, and for harder responses it can take longer.

Here are three examples from the Gemini diffusion model.

“What are the first 100 digits of pi?” This is actually 100 tokens, even though it looks like a short response. It only takes four steps to do that, because the model knows it's an easy prompt: you've just memorized the 100 digits of pi, so you can output it. Whereas in the same time an autoregressive model would have only done four tokens.

Slightly more challenging is to write a little bit of code, which takes about 18 forward passes to generate FizzBuzz.

Something more complicated, like “Explain quantum mechanics in a single paragraph,” took 31 denoising steps. It just took its time and decided to spend longer on that one.

So the model naturally gets to decide when it's going to finish and return the response. Typically, harder evals take more time. The evals are a year old now, so they're kind of old school, but on the harder end is GPQA Diamond, which for the model size we were targeting was quite a hard eval and took a long time to respond to. On the other end are things like MBPP, which are mostly basic Python programs and were very easy, so they took very little time to respond.

This is entirely determined by the model itself. Easier problems and prompts can be responded to quickly, and harder ones make it spend more time reasoning.

## Fast in-place editing

The last advantage is fast in-place editing.

Diffusion models in general have this very nice property where you can take an image, cut something out of it, or give it a prompt, and it'll fill it in. It can use the context you haven't cut out to fill in the missing piece correctly. You can use that for clever image editing.

The reason is that it's not autoregressive. There are autoregressive image generators that go left to right, top to bottom in raster order generating pixels, but diffusion doesn't work like that. It sees the entire image and then starts to denoise it. Because it gets to see every pixel, it can fill in the missing information and do it in a way that's consistent with the prompt.

We can do something similar for text. Here's one demo: it's just some code, and you say, “There is a bug in this code. Can you fix it?” It makes the edit in the correct place. You can barely see it, but it does a little fix to the indices.

You can say things like, “Can you add documentation?” and it goes in. It's not just generating all the tokens one by one. It's doing a clever editing procedure to fill in the correct edits. You can do that with more general text too: take a story and say, “Add a middle paragraph.” Because it can see the first and third paragraph, it can fill in the missing paragraph in a way that's consistent with the rest of the story. That's in-place editing.

## What low latency unlocks

The biggest advantage, like I mentioned, is low latency. We really lean into that. I want to show a couple of demos of things people internally have built to show what low latency can unlock. It's not just the same thing faster; it can unlock new applications.

You're all AI engineers, so it would be interesting to see when the next diffusion model comes out from our team what the low latency could unlock and what new applications can be built.

One demo is Wikipedia, where everything is generated on the fly, even the HTML. It's a web page with the HTML and the text being generated on the fly. It looks like regular Wikipedia, and when you click on it, the latency is low enough that it can just fill in the page as if it was a real Wikipedia page.

We have a similar thing for Reddit. Now all the responses to your posts will be by bots. They weren't already. It's generating fake comments. The Gemini diffusion model was not an image-generating model, so this demo links in the startup state-of-the-art image generator model at the time, which I think was Juno, before Nano Banana. The two models work together to fill in the web page. The image generation model is a little slower, but you can invent any Reddit you want — sharks in this case — and it'll generate the page with the text. The images follow a minute later, and then you can interact with this website as if it was a real website, with real users and so on. All the comments, all the images, all the HTML, everything is being generated entirely on the fly.

My favorite demo is an operating system also being entirely generated on the fly. Every click here is generating the next page of the operating system. It looks like a real operating system, but it's all being generated by the model on the fly in response to every click. When you enter the readme, it generates the text, but it also generates the web pages you can use to go back to the desktop and so on.

There's also a demo from someone on Twitter who used the Gemini diffusion web page to do live coding with his voice. He says:

> Create a to-do app.  
> Add 10 random to-dos.  
> Allow to-dos to have a completed state.  
> Mark four random to-dos as completed.  
> Allow me to sort to-do's by name and by state.  
> Sort by name, sort by state.  
> Testing, enter, was added to the bottom.  
> We'll try deleting a few.  
> Add one.  
> Everything's working.  
> Please convert this to dark mode.

And this was literally 15 seconds of work.

That was someone outside of our team, so he could say that. But I think low latency models can really unlock new experiences for users and new products. We're excited to see what people will do when the next generation comes out.

## Questions and answers

**Question:** Do you use all the same data?  
**Answer:** Yeah, we use all the same data. The algorithms have to change a bit, but we use all the same data. You can distill them.

**Question:** Are there any published ones?  
**Answer:** I'm not sure if there are any published ones. I don't think so. Maybe they're selling externally, but we're going to release something soon.

**Question:** Do bigger models require fewer steps for the same output?  
**Answer:** Yeah, the bigger models tend to require fewer steps for the same output. Even if the model is getting bigger and the FLOPs per forward pass are getting bigger, they tend to reduce the forward passes they need. So there's a kind of diminishing cost of serving even the biggest models.

**Question:** How do you price the structure?  
**Answer:** I don't know. We haven't got to that yet. I'm a research scientist.

**Question:** How do you define the size of the answer in coding or text?  
**Answer:** There are a few different ways. The easiest way is to fix some window length and then iterate on that. It's like autoregressive, block-wise autoregressive. That's the standard way to do it. But you can have a head that predicts the length of the response if you wanted.

**Question:** Do you have to fix the outcome in order to let the diffusion model work?  
**Answer:** No, it can still generate unlimited text. If you fix a window length, it just does that window length autoregressively if it needs to generate many windows of text.

**Question:** Can you set a limit on denoising steps ahead of time so you know your latency?  
**Answer:** Yeah, these are all with a limit, but they finish earlier than the limit.

**Question:** If you have multiple windows, can they go back and attempt previous windows?  
**Answer:** It's possible, but for us we just set it in stone and continue.

**Question:** How does prefill work?  
**Answer:** Prefill is the same. You've got some context and you prefill. After that, the generation step is typically in blocks of some fixed size, like 512 or 1,000 or 32 or whatever you want, and then that's autoregressive. The easiest way to do it is to just have a logits head at the top, just a vanilla prediction head.

**Question:** Is this all discrete diffusion?  
**Answer:** Yes, it's always tokens in, tokens out.

## Zmíněné odkazy a zdroje

- Google DeepMind
- Gemini diffusion
- Gemini 2.0 Flashlight
- Gemini 2.5 Flash
- ChatGPT-4o
- Claude
- Google I/O
- Wikipedia
- Reddit
- Juno
- Nano Banana
- GPQA Diamond
- MBPP