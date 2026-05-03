# Surprise Machines

![Surprise Machines visualization](assets/images/surprise-machines.jpg)

*Surprise Machines* is a data visualization that maps more than 213,000 digitized images from the Harvard Art Museums collection. It was created as part of *Curatorial A(i)gents*, an exhibition organized by metaLAB (at) Harvard in spring 2022, and asks what it means for a machine to curate — to surprise.

The project takes its name from Alan Turing, who, replying to Ada Lovelace's claim that machines are incapable of taking us by surprise, argued the opposite: that machines astonish us all the time, precisely through their unpredictability. Here, the surprise is one of scale. Visitors confront the vastness of a collection that cannot be hung on walls. Less than one percent of the 200,000-plus works ever finds its way into public view; the rest live in storage, in archives, in databases. *Surprise Machines* renders that hidden body visible.

## How it works

Each image was processed by an Inception convolutional neural network trained on ImageNet 2012, producing a high-dimensional vector that encodes its visual features. Those vectors were then projected into two dimensions with UMAP, which preserves local similarity — so visually related images settle near one another and the whole collection unfolds as a kind of nebula. The browser-side viewer, built on the open-source [PixPlot](https://github.com/YaleDHLab/pix-plot) tool by the Yale Digital Humanities Lab, draws all 213,000 cells with WebGL.

## Authors

Dario Rodighiero, Lins Derry, Douglas Duhaime, Jordan Kruguer, Maximilian C. Mueller, Christopher Pietsch, Jeffrey T. Schnapp, Jeff Steward, and metaLAB.

## Citation

Rodighiero, D., Derry, L., Duhaime, D., Kruguer, J., Mueller, M. C., Pietsch, C., Schnapp, J. T., Steward, J., & metaLAB. (2022). Surprise Machines: Revealing Harvard Art Museums' image collection. *Information Design Journal*, 27(1), 21–34. <https://doi.org/10.1075/idj.22013.rod>

## License

The viewer code is built on [PixPlot](https://github.com/YaleDHLab/pix-plot) by the Yale Digital Humanities Lab and is distributed under the MIT License (see `LICENSE`).

The article and accompanying text are available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The Harvard Art Museums collection — images, metadata, and provenance — remains the property of the Harvard Art Museums and is presented here for research and educational purposes.
