__author__ = 'mithrawnuruodo'


import gzip
import cStringIO

def decompressStringToFile(value, outputFile):
  """
  decompress the given string value (which must be valid compressed gzip
  data) and write the result in the given open file.
  """
  stream = cStringIO.StringIO(value)
  decompressor = gzip.GzipFile(fileobj=stream, mode='r')
  while True:  # until EOF
    chunk = decompressor.read(8192)
    if not chunk:
      decompressor.close()
      outputFile.close()
      return
    outputFile.write(chunk)


def decompressStringToString(value):
  """
  decompress the given string value (which must be valid compressed gzip
  data) and write the result in the given open file.
  """
  stream = cStringIO.StringIO(value)
  file = cStringIO.StringIO()
  decompressor = gzip.GzipFile(fileobj=stream, mode='r')
  while True:  # until EOF
    chunk = decompressor.read(8192)
    if not chunk:
      decompressor.close()
      #outputFile.close()
      return file
    file.write(chunk)
    #outputFile.write(chunk)


def compressFileToString(inputFile):
  """
  read the given open file, compress the data and return it as string.
  """
  stream = cStringIO.StringIO()
  compressor = gzip.GzipFile(fileobj=stream, mode='w')
  while True:  # until EOF
    chunk = inputFile.read(8192)
    if not chunk:  # EOF?
      compressor.close()
      return stream.getvalue()
    compressor.write(chunk)



if __name__=="__main__":

    path = "../Data/pimpstickv2.stl"
    file  = open(path, 'r')

    compressed = compressFileToString(file)

    path_out = "../Data/pimpstickv2_2.stl"
    file_out = open(path_out, 'w')

    decompressStringToFile(compressed, file_out)