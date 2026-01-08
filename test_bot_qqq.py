#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para verificar que el error "Precio inválido para QQQ" está resuelto
Simula exactamente el flujo del bot
"""

import asyncio
import logging
from unittest.mock import Mock, AsyncMock

logging.basicConfig(level=logging.WARNING)

# Importar el bot
from telegram_bot.bot import TelegramAnalystBot
from telegram import Update, Message, User, Chat
from telegram.ext import ContextTypes

async def test_qqq_analysis():
    """Test el comando /analizar QQQ exactamente como lo hace el bot"""
    
    print("\n" + "="*70)
    print("TEST: Simulating /analizar QQQ command")
    print("="*70)
    
    # Crear un mock de Update
    user = User(id=123, first_name="Test", is_bot=False)
    chat = Chat(id=456, type="private")
    message = Message(message_id=789, date=None, chat=chat)
    
    update = Mock(spec=Update)
    update.effective_chat = Mock()
    update.effective_chat.id = 456
    update.message = Mock()
    update.message.reply_text = AsyncMock(return_value=message)
    
    context = Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot = Mock()
    context.bot.send_chat_action = AsyncMock()
    context.args = ["QQQ"]  # Simular /analizar QQQ
    context.user_data = {}
    
    # Crear el bot
    bot = TelegramAnalystBot()
    
    # Ejecutar el análisis
    try:
        await bot.comando_analizar(update, context)
        
        # Verificar si hubo error
        call_args = update.message.reply_text.call_args_list
        
        if call_args:
            last_call_text = call_args[-1][0][0]  # Último mensaje enviado
            
            if "Error en análisis" in last_call_text:
                print(f"FAILED: Got error message:")
                print(last_call_text)
                return False
            else:
                print(f"SUCCESS: No error message")
                print(f"Analysis completed successfully")
                return True
        else:
            print("ERROR: No message was sent")
            return False
            
    except Exception as e:
        print(f"EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_qqq_analysis())
    
    print("\n" + "="*70)
    if result:
        print("TEST RESULT: PASSED")
    else:
        print("TEST RESULT: FAILED")
    print("="*70)
