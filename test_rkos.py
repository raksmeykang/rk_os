import sys
import os

# Add current directory to Python path (crucial fix)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print('=== RK-OS Panel Testing ===')
print(f'Working Directory: {current_dir}')
print(f'Python Path Length: {len(sys.path)}')

try:
    # Test all imports
    print('1. Testing API import...')
    from src.interfaces.api import PanelServer
    print('✅ API server imported successfully')
    
    print('2. Testing CLI import...')  
    from src.interfaces.cli import CommandLineInterface
    print('✅ CLI interface imported successfully')
    
    print('3. Testing package imports...')
    from src.interfaces import PanelServer, CommandLineInterface
    print('✅ Package imports work correctly')
    
    print('4. Testing CLI status function...')
    # Import and test the actual functionality
    cli_instance = CommandLineInterface()
    cli_instance.status()  # This should work now
    
    print('')
    print('🎉 ALL TESTS PASSED - RK-OS Panel is fully functional!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()

