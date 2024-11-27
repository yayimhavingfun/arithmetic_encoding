from decimal import Decimal, getcontext, InvalidOperation
import math

def calculate_probabilities(message):
    frequency = {}
    for symbol in message:
        if symbol in frequency:
            frequency[symbol] += 1
        else:
            frequency[symbol] = 1

    total_count = sum(frequency.values())
    probabilities = {symbol: Decimal(count) / Decimal(total_count) for symbol, count in frequency.items()}
    return probabilities


def arithmetic_encoding(message, precision=50):
    # установка точности
    getcontext().prec = precision

    probabilities = calculate_probabilities(message)
    sorted_probabilities = dict(sorted(probabilities.items(), key=lambda item: item[1]))

    cumulative_prob = {}
    cumulative = Decimal(0)

    for symbol, prob in sorted_probabilities.items():
        cumulative_prob[symbol] = (cumulative, cumulative + prob)
        cumulative += prob

    # кодирование
    print("start: (0, 1)")
    low, high = Decimal(0), Decimal(1)
    for symbol in message:
        symbol_low, symbol_high = cumulative_prob[symbol]
        range_width = high - low
        high = low + range_width * symbol_high
        low = low + range_width * symbol_low
        print(f"{symbol}: [{low}, {high})")

        # подсчет q и p
    range_width = high - low
    q = -math.floor(math.log2(float(range_width)))
    p = math.floor(float(low) * (2 ** q))

    # убедимся что p/2^q находится в [0, 1)
    while True:
        encoded_value = Decimal(p) / Decimal(2 ** q)
        if low <= encoded_value < high:
            break
        p += 1

    return (p, q), low, high

message = input("Insert message to encode: ")
(p, q), final_low, final_high = arithmetic_encoding(message)
print("========")
print(f"Encoded value: {p} / 2^{q}")
print(f"Binary encoding: {p}\u2081\u2080 = {bin(p)[2:].zfill(q)}\u2082")
print(f"Final range: [{final_low}, {final_high})")
