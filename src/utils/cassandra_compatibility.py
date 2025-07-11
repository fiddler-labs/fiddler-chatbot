"""
Cassandra Driver Compatibility Layer for Python 3.13+

This module provides compatibility for the Cassandra driver when running on 
Python 3.13+, where the asyncore module has been removed. It creates a 
comprehensive asyncore compatibility layer and handles connection class imports.
"""

import sys
from typing import Optional, Any


def setup_asyncore_compatibility() -> None:
    """
    Set up asyncore compatibility layer for Python 3.13+
    """
    try:
        import asyncore  # type: ignore
        print("✅ Native asyncore module available")
        return
    except ImportError:
        pass
    
    # Create a comprehensive asyncore compatibility layer
    import types
    import socket
    import select
    import errno
    
    # Create a comprehensive asyncore module
    asyncore_module = types.ModuleType('asyncore')
    
    # Add socket map for tracking connections
    socket_map = {}
    
    # Add minimal required classes/functions
    class dispatcher:
        def __init__(self, sock=None, map=None):
            self.socket = sock
            self.map = map if map is not None else socket_map
            self.connected = False
            self.accepting = False
            self.closing = False
            self.addr = None
            
        def close(self):
            self.closing = True
            if self.socket:
                self.socket.close()
            if self in self.map:
                del self.map[self]
                
        def set_socket(self, sock):
            self.socket = sock
            
        def handle_connect(self):
            self.connected = True
            
        def handle_close(self):
            self.close()
            
        def handle_read(self):
            pass
            
        def handle_write(self):
            pass
            
        def readable(self):
            return True
            
        def writable(self):
            return True
            
        def handle_error(self):
            pass
    
    # Add loop function
    def loop(timeout=30.0, map=None, use_poll=False, count=None):
        '''Comprehensive asyncore.loop implementation'''
        if map is None:
            map = socket_map
            
        if not map:
            return
            
        # Simple select-based loop
        for i in range(count or 1):
            if not map:
                break
                
            r = []
            w = []
            e = []
            
            for fd, obj in map.items():
                if hasattr(obj, 'readable') and obj.readable():
                    r.append(fd)
                if hasattr(obj, 'writable') and obj.writable():
                    w.append(fd)
                e.append(fd)
                
            if not (r or w or e):
                break
                
            try:
                r, w, e = select.select(r, w, e, timeout)
                
                for fd in r:
                    if fd in map:
                        try:
                            map[fd].handle_read()
                        except Exception:
                            map[fd].handle_error()
                            
                for fd in w:
                    if fd in map:
                        try:
                            map[fd].handle_write()
                        except Exception:
                            map[fd].handle_error()
                            
                for fd in e:
                    if fd in map:
                        try:
                            map[fd].handle_error()
                        except Exception:
                            pass
                            
            except select.error as err:
                if err.args[0] == errno.EINTR:
                    continue
                raise
    
    # Add close_all function
    def close_all(map=None):
        if map is None:
            map = socket_map
        for obj in list(map.values()):
            obj.close()
    
    # Use setattr to avoid linter errors
    setattr(asyncore_module, 'dispatcher', dispatcher)
    setattr(asyncore_module, 'socket_map', socket_map)
    setattr(asyncore_module, 'loop', loop)
    setattr(asyncore_module, 'close_all', close_all)
    
    # Add the module to sys.modules
    sys.modules['asyncore'] = asyncore_module
    print("✅ Created comprehensive asyncore compatibility layer for Python 3.13")


def setup_cassandra_connection_classes() -> Optional[Any]:
    """
    Setup and return the best available Cassandra connection class
    
    Returns:
        Connection class or None if using default
    """
    connection_classes = []
    
    # Try LibevConnection first
    try:
        from cassandra.io.libevreactor import LibevConnection
        connection_classes.append(LibevConnection)
        print("✅ LibevConnection available")
    except Exception as e:
        print(f"⚠️  LibevConnection not available: {e}")
    
    # Try AsyncoreConnection as fallback
    try:
        from cassandra.io.asyncorereactor import AsyncoreConnection
        connection_classes.append(AsyncoreConnection)
        print("✅ AsyncoreConnection available")
    except Exception as e:
        print(f"⚠️  AsyncoreConnection not available: {e}")
    
    # Try EventletConnection as another fallback
    try:
        from cassandra.io.eventletreactor import EventletConnection
        connection_classes.append(EventletConnection)
        print("✅ EventletConnection available")
    except Exception as e:
        print(f"⚠️  EventletConnection not available: {e}")
        
    # Try TwistedConnection as last resort
    try:
        from cassandra.io.twistedreactor import TwistedConnection
        connection_classes.append(TwistedConnection)
        print("✅ TwistedConnection available")
    except Exception as e:
        print(f"⚠️  TwistedConnection not available: {e}")
    
    # Use the first available connection class
    if connection_classes:
        cassandra_connection_class = connection_classes[0]
        print(f"✅ Using connection class: {cassandra_connection_class.__name__}")
        return cassandra_connection_class
    else:
        print("⚠️  No connection classes available, using default")
        return None


def setup_cassandra_compatibility() -> tuple[Any, Any, Any, Any, Optional[Any]]:
    """
    Complete Cassandra compatibility setup
    
    Returns:
        tuple: (Cluster, Session, PlainTextAuthProvider, named_tuple_factory, connection_class)
    """
    # CONDITIONAL - only if using Python 3.12 onwards
    # setup_asyncore_compatibility()
    
    try:
        from cassandra.cluster import Cluster, Session
        from cassandra.auth import PlainTextAuthProvider
        from cassandra.query import named_tuple_factory
        print("✅ Successfully imported basic Cassandra components")
    except Exception as e:
        print(f"❌ Failed to import basic Cassandra components: {e}")
        raise
    
    # Get the best connection class
    connection_class = setup_cassandra_connection_classes()
    
    print("✅ Cassandra compatibility setup complete")
    return Cluster, Session, PlainTextAuthProvider, named_tuple_factory, connection_class 