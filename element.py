class Element: # 1 or 2 dimensional element
    def __init__(self, name, *attributes):
        if len(attributes) not in (1,2):
            raise ValueError(f"Dimensions should be 1 or 2.")
        self.attributes = attributes  
        self.name = name
        
    def __hash__(self) -> int:
        return hash(self.attributes)

