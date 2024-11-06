location = 0xFFFFFFFF  # Example initial value with all bits set to 1
x = 12345678           # Example 26-bit value

# Set first 26 bits of location to x
location = (location & ~((1 << 26) - 1)) | (x & ((1 << 26) - 1))

print(f"Modified location: {bin(location)}")
