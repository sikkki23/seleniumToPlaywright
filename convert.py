import os
import re
import yaml
from pathlib import Path

class JavaToPlaywrightConverter:
    def __init__(self, rules_file='mapping_rules.yaml'):
        with open(rules_file, 'r') as f:
            self.rules = yaml.safe_load(f)
    
    def convert_line(self, line):
        # Apply class/method declarations
        if re.search(self.rules['class_declaration']['pattern'], line):
            match = re.search(self.rules['class_declaration']['pattern'], line)
            class_name = match.group(1)
            return self.rules['class_declaration']['replacement'].format(lower_name=class_name.lower())
        
        # Apply test method conversion
        if re.search(self.rules['method_declaration']['pattern'], line):
            match = re.search(self.rules['method_declaration']['pattern'], line)
            return self.rules['method_declaration']['replacement'].format(name=match.group(1).lower())
        
        # Handle element interactions
        for rule in self.rules['element_interaction']:
            match = re.search(rule['pattern'], line)
            if match:
                locator = match.group(1).replace('"', '')
                action = match.group(2)
                args = match.group(3).strip('"') if match.group(3) else ""
                
                if action in rule['actions']:
                    return rule['actions'][action].format(locator=locator, text=args)
        
        # Apply simple regex replacements
        for rule_type in ['navigation', 'driver_initialization', 'cleanup']:
            rule = self.rules[rule_type]
            match = re.search(rule['pattern'], line)
            if match:
                return rule['replacement'].format(**match.groupdict())
        
        return line  # Return unchanged if no match
    
    def convert_file(self, java_path, output_dir):
        with open(java_path, 'r') as f:
            java_lines = f.readlines()
        
        python_lines = []
        for line in java_lines:
            converted = self.convert_line(line.strip())
            if converted:
                python_lines.append(converted)
        
        py_filename = os.path.basename(java_path).replace('.java', '.py')
        output_path = os.path.join(output_dir, py_filename)
        
        with open(output_path, 'w') as f:
            f.write("\n".join(python_lines))

if __name__ == "__main__":
    converter = JavaToPlaywrightConverter()
    input_dir = 'input_java_tests'
    output_dir = 'converted_python_tests'
    
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.java'):
            java_path = os.path.join(input_dir, filename)
            converter.convert_file(java_path, output_dir)