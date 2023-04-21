import noise


class NoiseFactory:
    def __init__(self, noise_type: str):
        self.noise_type = noise_type

    def waarde(self, x, y, octaves, persistence, lacunarity, repeatx, repeaty, base):
        if self.noise_type == "perlin":
            return (noise.pnoise2(x,
                                  y,
                                  octaves=octaves,
                                  persistence=persistence,
                                  lacunarity=lacunarity,
                                  repeatx=repeatx,
                                  repeaty=repeaty,
                                  base=base))
        elif self.noise_type == "simplex":
            return (noise.snoise2(x,
                                  y,
                                  octaves=octaves,
                                  persistence=persistence,
                                  lacunarity=lacunarity,
                                  repeatx=repeatx,
                                  repeaty=repeaty,
                                  base=base))
        else:
            raise ValueError(f'Kies noise uit "perlin" of "simplex", {self.noise_type} bestaat niet')
            print(f"{self.noise_type} bestaat niet")

