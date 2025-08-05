import json
from typing import Any


def try_pretty_formatting(data: Any, max_depth: int = 6, max_items: int = 50, indent_size: int = 2, current_depth: int = 0) -> str:
    """
    World-class utility for formatting any data type into human-readable format.
    
    Handles everything from simple strings to complex nested objects like ChatbotState,
    LangChain messages, and deeply nested data structures with intelligent formatting.
    
    Args:
        data: Any data type to format
        max_depth: Maximum recursion depth to prevent infinite loops
        max_items: Maximum items to show in collections before truncating
        indent_size: Number of spaces per indentation level
        current_depth: Current recursion depth (internal use)
    
    Returns:
        Beautifully formatted string representation
    """
    indent = " " * (current_depth * indent_size)
    next_indent = " " * ((current_depth + 1) * indent_size)
    
    # Depth limit check
    if current_depth >= max_depth:
        return f"{indent}... (max depth {max_depth} reached)"
    
    # Handle None
    if data is None:
        return "None"
    
    # Handle basic types
    if isinstance(data, (bool, int, float)):
        return str(data)
    
    # Handle strings with special formatting for multiline
    if isinstance(data, str):
        if len(data) > 100 or '\n' in data:
            lines = data.split('\n')
            if len(lines) == 1:
                # Long single line
                return f'"{data[:100]}{"..." if len(data) > 100 else ""}"'
            else:
                # Multiline string
                formatted_lines = [f"{next_indent}{line}" for line in lines[:10]]
                if len(lines) > 10:
                    formatted_lines.append(f"{next_indent}... ({len(lines) - 10} more lines)")
                return f'"""\n{chr(10).join(formatted_lines)}\n{indent}"""'
        return f'"{data}"'
    
    # Handle bytes
    if isinstance(data, bytes):
        preview = data[:50].decode('utf-8', errors='replace')
        return f'bytes({len(data)}): "{preview}{"..." if len(data) > 50 else ""}"'
    
    # Handle functions and classes
    if callable(data):
        if hasattr(data, '__name__'):
            return f"<{type(data).__name__}: {data.__name__}>"
        return f"<{type(data).__name__}>"
    
    # Handle types
    if isinstance(data, type):
        return f"<class '{data.__name__}'>"
    
    # Handle lists and tuples
    if isinstance(data, (list, tuple)):
        if not data:
            return "[]" if isinstance(data, list) else "()"
        
        type_name = "list" if isinstance(data, list) else "tuple"
        items = []
        
        for i, item in enumerate(data):
            if i >= max_items:
                items.append(f"{next_indent}... ({len(data) - max_items} more items)")
                break
            formatted_item = try_pretty_formatting(
                item, max_depth, max_items, indent_size, current_depth + 1
            )
            # Add proper indentation to multiline items
            if '\n' in formatted_item:
                formatted_item = formatted_item.replace('\n', f'\n{next_indent}')
            items.append(f"{next_indent}{formatted_item}")
        
        bracket_open = "[" if isinstance(data, list) else "("
        bracket_close = "]" if isinstance(data, list) else ")"
        
        return f"{type_name}({len(data)}) {bracket_open}\n{chr(10).join(items)}\n{indent}{bracket_close}"
    
    # Handle sets
    if isinstance(data, set):
        if not data:
            return "set()"
        items = []
        for i, item in enumerate(sorted(data, key=lambda x: str(x)) if len(data) <= max_items else list(data)[:max_items]):
            if i >= max_items:
                items.append(f"{next_indent}... ({len(data) - max_items} more items)")
                break
            formatted_item = try_pretty_formatting(
                item, max_depth, max_items, indent_size, current_depth + 1
            )
            items.append(f"{next_indent}{formatted_item}")
        
        return f"set({len(data)}) {{\n{chr(10).join(items)}\n{indent}}}"
    
    # Handle dictionaries
    if isinstance(data, dict):
        if not data:
            return "{}"
        
        items = []
        for i, (key, value) in enumerate(data.items()):
            if i >= max_items:
                items.append(f"{next_indent}... ({len(data) - max_items} more items)")
                break
            
            # Format key
            formatted_key = try_pretty_formatting(
                key, max_depth, max_items, indent_size, current_depth + 1
            )
            if '\n' in formatted_key:
                formatted_key = formatted_key.replace('\n', f'\n{next_indent}')
            
            # Format value
            formatted_value = try_pretty_formatting(
                value, max_depth, max_items, indent_size, current_depth + 1
            )
            if '\n' in formatted_value:
                formatted_value = formatted_value.replace('\n', f'\n{next_indent}')
            
            items.append(f"{next_indent}{formatted_key}: {formatted_value}")
        
        return f"dict({len(data)}) {{\n{chr(10).join(items)}\n{indent}}}"
    
    # Handle LangChain BaseMessage objects specially
    if hasattr(data, '__class__') and 'BaseMessage' in str(data.__class__.__mro__):
        msg_type = data.__class__.__name__
        content_preview = str(data.content)[:200] if hasattr(data, 'content') else "No content"
        if len(content_preview) > 200:
            content_preview += "..."
        
        attrs = []
        if hasattr(data, 'content'):
            attrs.append(f"{next_indent}content: {try_pretty_formatting(data.content, max_depth, max_items, indent_size, current_depth + 1)}")
        if hasattr(data, 'additional_kwargs') and data.additional_kwargs:
            attrs.append(f"{next_indent}additional_kwargs: {try_pretty_formatting(data.additional_kwargs, max_depth, max_items, indent_size, current_depth + 1)}")
        if hasattr(data, 'tool_calls') and data.tool_calls:
            attrs.append(f"{next_indent}tool_calls: {try_pretty_formatting(data.tool_calls, max_depth, max_items, indent_size, current_depth + 1)}")
        if hasattr(data, 'name') and data.name:
            attrs.append(f"{next_indent}name: {data.name}")
        
        return f"{msg_type} {{\n{chr(10).join(attrs)}\n{indent}}}"
    
    # Handle dataclasses
    if hasattr(data, '__dataclass_fields__'):
        class_name = data.__class__.__name__
        fields = []
        for field_name in data.__dataclass_fields__:
            try:
                field_value = getattr(data, field_name)
                formatted_value = try_pretty_formatting(
                    field_value, max_depth, max_items, indent_size, current_depth + 1
                )
                if '\n' in formatted_value:
                    formatted_value = formatted_value.replace('\n', f'\n{next_indent}')
                fields.append(f"{next_indent}{field_name}: {formatted_value}")
            except Exception as e:
                fields.append(f"{next_indent}{field_name}: <Error accessing: {e}>")
        
        return f"{class_name} {{\n{chr(10).join(fields)}\n{indent}}}"
    
    # Handle objects with __dict__
    if hasattr(data, '__dict__'):
        class_name = data.__class__.__name__
        obj_dict = data.__dict__
        
        if not obj_dict:
            return f"{class_name}()"
        
        attrs = []
        for i, (attr_name, attr_value) in enumerate(obj_dict.items()):
            if i >= max_items:
                attrs.append(f"{next_indent}... ({len(obj_dict) - max_items} more attributes)")
                break
            
            # Skip private attributes unless they're important
            if attr_name.startswith('_') and not attr_name.startswith('__'):
                continue
                
            formatted_value = try_pretty_formatting(
                attr_value, max_depth, max_items, indent_size, current_depth + 1
            )
            if '\n' in formatted_value:
                formatted_value = formatted_value.replace('\n', f'\n{next_indent}')
            attrs.append(f"{next_indent}{attr_name}: {formatted_value}")
        
        if not attrs:
            return f"{class_name}()"
        
        return f"{class_name} {{\n{chr(10).join(attrs)}\n{indent}}}"
    
    # Handle objects with __slots__
    if hasattr(data, '__slots__'):
        class_name = data.__class__.__name__
        attrs = []
        
        for slot_name in data.__slots__:
            try:
                if hasattr(data, slot_name):
                    slot_value = getattr(data, slot_name)
                    formatted_value = try_pretty_formatting(
                        slot_value, max_depth, max_items, indent_size, current_depth + 1
                    )
                    if '\n' in formatted_value:
                        formatted_value = formatted_value.replace('\n', f'\n{next_indent}')
                    attrs.append(f"{next_indent}{slot_name}: {formatted_value}")
            except Exception as e:
                attrs.append(f"{next_indent}{slot_name}: <Error accessing: {e}>")
        
        if not attrs:
            return f"{class_name}()"
        
        return f"{class_name} {{\n{chr(10).join(attrs)}\n{indent}}}"
    
    # Last resort: try JSON serialization for JSON-serializable objects
    try:
        json_str = json.dumps(data, indent=indent_size, default=str, ensure_ascii=False)
        # Add proper indentation to each line
        lines = json_str.split('\n')
        indented_lines = [f"{indent}{line}" if i > 0 else line for i, line in enumerate(lines)]
        return '\n'.join(indented_lines)
    except Exception:
        pass
    
    # Final fallback: string representation with class info
    try:
        obj_str = str(data)
        class_name = data.__class__.__name__
        if len(obj_str) > 200:
            obj_str = obj_str[:200] + "..."
        return f"{class_name}: {obj_str}"
    except Exception:
        pass
    
    # Ultimate fallback
    try:
        return f"<{type(data).__name__} object at {hex(id(data))}>"
    except Exception:
        return "<unprintable object>"
        