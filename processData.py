import json
import pandas

def process(raw):
    rawData = {
        "aqi": {
            "-M-ng7WuphLat21sn9te": {
            "time": "11-02-2020 15:29:25",
            "value": 31
            },
            "-M-ngCRKxwsR2aHlsDiw": {
            "time": "11-02-2020 15:29:46",
            "value": 44
            },
            "-M-ngHsG53MFIXPPll2r": {
            "time": "11-02-2020 15:30:07",
            "value": 31
            },
            "-M-ngMd5EPh7qHsdpzji": {
            "time": "11-02-2020 15:30:28",
            "value": 26
            },
            "-M-ngRTCfS5Uv9A3gayf": {
            "time": "11-02-2020 15:30:47",
            "value": 28
            },
            "-M-ngWXhkh_wN6mB5ZcF": {
            "time": "11-02-2020 15:31:07",
            "value": 37
            },
            "-M-ngaIeylQwC3zDIE3z": {
            "time": "11-02-2020 15:31:28",
            "value": 28
            },
            "-M-ngfPsq7ZfwTkg9A_K": {
            "time": "11-02-2020 15:31:43",
            "value": 26
            },
            "-M-ngm3vzRnkC9CpZAEf": {
            "time": "11-02-2020 15:32:11",
            "value": 35
            },
            "-M-ngsuKm1lMuxA_8Jrf": {
            "time": "11-02-2020 15:32:38",
            "value": 44
            }
        },
        "humidity": {
            "-M-ng6YzxwOlAoZIW0id": {
            "time": "11-02-2020 15:29:25",
            "value": 25
            },
            "-M-ngBWfNTm_XYCVWX2X": {
            "time": "11-02-2020 15:29:46",
            "value": 37
            },
            "-M-ngGmouCd9xmkQgWS0": {
            "time": "11-02-2020 15:30:07",
            "value": 34
            },
            "-M-ngLnHEaxZxn8ONp65": {
            "time": "11-02-2020 15:30:28",
            "value": 43
            },
            "-M-ngQWKhKbyJ2DUcMvI": {
            "time": "11-02-2020 15:30:47",
            "value": 36
            },
            "-M-ngVbfm2isiwhIGQJ4": {
            "time": "11-02-2020 15:31:07",
            "value": 27
            },
            "-M-ng_O50O3WaAhJvSyN": {
            "time": "11-02-2020 15:31:28",
            "value": 39
            },
            "-M-ngdq7L6m-1CQZi5cr": {
            "time": "11-02-2020 15:31:43",
            "value": 38
            },
            "-M-ngkWG8WVnoNLUoIfx": {
            "time": "11-02-2020 15:32:11",
            "value": 42
            },
            "-M-ngr7OqS1wYfDWoJHE": {
            "time": "11-02-2020 15:32:38",
            "value": 41
            }
        },
        "pm10": {
            "-M-ng76g4OXxkPNgbIcH": {
            "time": "11-02-2020 15:29:25",
            "value": 26
            },
            "-M-ngC8c88yduhxoGy3K": {
            "time": "11-02-2020 15:29:46",
            "value": 40
            },
            "-M-ngHVkscyMAgYosv3V": {
            "time": "11-02-2020 15:30:07",
            "value": 32
            },
            "-M-ngMMUhqaZFcdeJP4t": {
            "time": "11-02-2020 15:30:28",
            "value": 33
            },
            "-M-ngRAzkzidS1HSRs9X": {
            "time": "11-02-2020 15:30:47",
            "value": 44
            },
            "-M-ngWGvDWDU_8tEjEzE": {
            "time": "11-02-2020 15:31:07",
            "value": 28
            },
            "-M-ng_zxyNiC9GfJFiGy": {
            "time": "11-02-2020 15:31:28",
            "value": 35
            },
            "-M-ngeupXsCKQBfTd4uN": {
            "time": "11-02-2020 15:31:43",
            "value": 42
            },
            "-M-nglXzUTGSvsYij727": {
            "time": "11-02-2020 15:32:11",
            "value": 35
            },
            "-M-ngsPlA8Poc9gJTIR3": {
            "time": "11-02-2020 15:32:38",
            "value": 43
            }
        },
        "pm25": {
            "-M-ng6qlNjyO-_boRVe3": {
            "time": "11-02-2020 15:29:25",
            "value": 43
            },
            "-M-ngBpN_4XVA3Uf9dYl": {
            "time": "11-02-2020 15:29:46",
            "value": 34
            },
            "-M-ngH3zWLIEIXz965Dw": {
            "time": "11-02-2020 15:30:07",
            "value": 36
            },
            "-M-ngM2kxUFPKbSMelSO": {
            "time": "11-02-2020 15:30:28",
            "value": 36
            },
            "-M-ngQuV3dNlRXXUyDwt": {
            "time": "11-02-2020 15:30:47",
            "value": 41
            },
            "-M-ngVy2uxeUJFRhdEjp": {
            "time": "11-02-2020 15:31:07",
            "value": 43
            },
            "-M-ng_etmiiGh7LAo-J5": {
            "time": "11-02-2020 15:31:28",
            "value": 28
            },
            "-M-ngeNh0wIELeOxX2wS": {
            "time": "11-02-2020 15:31:43",
            "value": 25
            },
            "-M-ngkzKq9AZJPRZO1gX": {
            "time": "11-02-2020 15:32:11",
            "value": 27
            },
            "-M-ngrtvfyZWUsPvdvj8": {
            "time": "11-02-2020 15:32:38",
            "value": 29
            }
        },
        "temp": {
            "-M-ng6Ce77YhSECU4QP-": {
            "time": "11-02-2020 15:29:25",
            "value": 41
            },
            "-M-ngBGCII8Yi1co_mn_": {
            "time": "11-02-2020 15:29:46",
            "value": 37
            },
            "-M-ngGRWQbME6IDBx1dv": {
            "time": "11-02-2020 15:30:07",
            "value": 42
            },
            "-M-ngLV5eQODeQDYmrQ3": {
            "time": "11-02-2020 15:30:28",
            "value": 36
            },
            "-M-ngQChq2lV4-wKscGW": {
            "time": "11-02-2020 15:30:47",
            "value": 27
            },
            "-M-ngV67CDDL_OItrdEb": {
            "time": "11-02-2020 15:31:07",
            "value": 26
            },
            "-M-ng_398krE1DCf64_O": {
            "time": "11-02-2020 15:31:28",
            "value": 28
            },
            "-M-ngdOdJ4PZNNmR4seN": {
            "time": "11-02-2020 15:31:43",
            "value": 38
            },
            "-M-ngjyGWcOCL4r1dq8A": {
            "time": "11-02-2020 15:32:11",
            "value": 30
            },
            "-M-ngqV82Ue57VdARpfP": {
            "time": "11-02-2020 15:32:38",
            "value": 35
            }
        }
    }
    # rawData = json.dumps(rawData)
    print(json.dumps(rawData["temp"], indent=2))
    return raw

k = process("hello")