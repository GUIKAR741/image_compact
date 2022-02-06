"""."""
import click
import cv2
import os
from lzw_compress import comprimir
from lzw_decompress import decompress


@click.group()
def cli():
    """."""
    pass


@cli.command()
@click.option('-i', "--input-file", help="Arquivo a ser comprimido.")
@click.option("-o", '--output-file', help="Arquivo de saida.")
def compress_file(input_file, output_file):
    """Comprimir o arquivo."""
    if os.path.isfile(input_file):
        image = cv2.imread(input_file)
        x, y = image.shape[:2][::-1]
        xr, yr = int(x - (x * .25)), int(y - (y * .25))
        image = cv2.resize(image, (xr, yr), interpolation=cv2.INTER_LINEAR)
        tmp = '_tmp_' + input_file
        cv2.imwrite(tmp, image)
        comprimir(tmp, f"{x}_{y}_{output_file}")
        os.remove(tmp)
    else:
        print("Arquivo inexistente.")


@cli.command()
@click.option('-i', "--input-file", help="Arquivo a ser descomprimido.")
@click.option("-o", '--output-file', help="Arquivo de saida.")
def decompress_file(input_file, output_file):
    """Descomprimir o arquivo."""
    if os.path.isfile(input_file) and len(input_file.split('_')) == 3:
        x, y = input_file.split('_')[:2]
        x, y = int(x), int(y)
        decompress(input_file, output_file)
        image = cv2.imread(output_file)
        image = cv2.resize(image, (x, y), interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(output_file, image)
    else:
        print("Arquivo inexistente ou não possui parametros de tamanho.")


if __name__ == '__main__':
    cli()
