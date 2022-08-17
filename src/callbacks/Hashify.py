from typing import Callable
import mmh3


hashify_by_murmurhash_64bits: Callable = lambda px: bin(mmh3.hash64(str(px))[0])[2:]
hashify_by_murmurhash_128bits: Callable = lambda px: bin(mmh3.hash128(str(px)))[2:]
