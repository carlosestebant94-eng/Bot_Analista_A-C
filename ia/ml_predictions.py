"""
ia/ml_predictions.py
Machine Learning para predicciones de mercado
Entrena modelos para predecir:
1. Accuracy de analistas
2. Probabilidad de movimiento al alza/baja
3. Volatilidad futura
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Any, Optional
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle
import os

logger = logging.getLogger("MLPredictions")


class MLPredictor:
    """Predictor de ML para mercado financiero"""
    
    def __init__(self, model_dir: str = "models"):
        """
        Inicializa el predictor de ML
        
        Args:
            model_dir: Directorio para guardar/cargar modelos
        """
        self.logger = logging.getLogger("MLPredictor")
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
        # Modelos
        self.price_direction_model = None  # Predice si sube/baja
        self.volatility_model = None        # Predice volatilidad futura
        self.analyst_accuracy_model = None  # Predice accuracy de analistas
        self.confidence_model = None        # Predice confianza general
        
        # Scalers
        self.scaler = StandardScaler()
        
        # Cargar modelos si existen
        self._load_models()
        
        self.logger.info("✅ ML Predictor inicializado")
    
    def train_models(self, historical_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Entrena todos los modelos con datos históricos
        
        Args:
            historical_data: Dict con DataFrames históricos por ticker
                            {'AAPL': df, 'MSFT': df, ...}
        
        Returns:
            Dict con métricas de entrenamiento
        """
        try:
            self.logger.info(f"🤖 Entrenando modelos con {len(historical_data)} tickers...")
            
            # Preparar features de todos los datos
            X_all, y_direction_all, y_volatility_all = [], [], []
            
            for ticker, df in historical_data.items():
                if len(df) < 100:
                    self.logger.warning(f"⚠️  {ticker} tiene menos de 100 datos, saltando...")
                    continue
                
                X, y_direction, y_volatility = self._extract_features(df)
                
                if X is not None:
                    X_all.append(X)
                    y_direction_all.append(y_direction)
                    y_volatility_all.append(y_volatility)
            
            if not X_all:
                return {"error": "No hay datos suficientes para entrenar"}
            
            # Combinar todos los datos
            X_combined = np.vstack(X_all)
            y_direction_combined = np.concatenate(y_direction_all)
            y_volatility_combined = np.concatenate(y_volatility_all)
            
            # Normalizar features
            X_scaled = self.scaler.fit_transform(X_combined)
            
            # Split train/test
            X_train, X_test, y_dir_train, y_dir_test, y_vol_train, y_vol_test = train_test_split(
                X_scaled, y_direction_combined, y_volatility_combined,
                test_size=0.2, random_state=42
            )
            
            # Entrenar modelo de dirección de precio
            self.logger.info("  📈 Entrenando modelo de dirección de precio...")
            self.price_direction_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                random_state=42,
                n_jobs=-1
            )
            self.price_direction_model.fit(X_train, y_dir_train)
            acc_direction = self.price_direction_model.score(X_test, y_dir_test)
            
            # Entrenar modelo de volatilidad
            self.logger.info("  📊 Entrenando modelo de volatilidad...")
            self.volatility_model = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
            self.volatility_model.fit(X_train, y_vol_train)
            acc_volatility = self.volatility_model.score(X_test, y_vol_test)
            
            # Entrenar modelo de confianza (basado en características)
            self.logger.info("  🎯 Entrenando modelo de confianza...")
            y_confidence = self._calculate_confidence_labels(X_combined)
            X_train_conf, X_test_conf, y_conf_train, y_conf_test = train_test_split(
                X_scaled, y_confidence, test_size=0.2, random_state=42
            )
            self.confidence_model = GradientBoostingClassifier(
                n_estimators=50,
                max_depth=5,
                random_state=42
            )
            self.confidence_model.fit(X_train_conf, y_conf_train)
            acc_confidence = self.confidence_model.score(X_test_conf, y_conf_test)
            
            # Guardar modelos
            self._save_models()
            
            resultado = {
                "status": "completado",
                "modelos_entrenados": 3,
                "accuracy_price_direction": round(acc_direction, 4),
                "accuracy_volatility": round(acc_volatility, 4),
                "accuracy_confidence": round(acc_confidence, 4),
                "samples_entrenamiento": len(X_train),
                "samples_validacion": len(X_test),
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"✅ Modelos entrenados exitosamente")
            self.logger.info(f"   - Price Direction Accuracy: {acc_direction:.4f}")
            self.logger.info(f"   - Volatility Accuracy: {acc_volatility:.4f}")
            self.logger.info(f"   - Confidence Accuracy: {acc_confidence:.4f}")
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"❌ Error entrenando modelos: {str(e)}")
            return {"error": str(e)}
    
    def predict_price_direction(self, ticker: str, current_indicators: Dict) -> Dict[str, Any]:
        """
        Predice la dirección probable del precio (sube/baja)
        
        Args:
            ticker: Símbolo del instrumento
            current_indicators: Dict con indicadores técnicos actuales
        
        Returns:
            Dict con predicción y confianza
        """
        try:
            if self.price_direction_model is None:
                return {"error": "Modelo no entrenado", "disponible": False}
            
            # Extraer features del indicador
            features = self._extract_features_from_indicators(current_indicators)
            features_scaled = self.scaler.transform([features])
            
            # Predicción
            prediction = self.price_direction_model.predict(features_scaled)[0]
            probability = self.price_direction_model.predict_proba(features_scaled)[0]
            
            direction = "ALCISTA" if prediction == 1 else "BAJISTA"
            confidence = float(max(probability))
            
            return {
                "ticker": ticker,
                "direccion_predicha": direction,
                "confianza": round(confidence, 4),
                "probabilidad_alcista": round(probability[1] if len(probability) > 1 else probability[0], 4),
                "probabilidad_bajista": round(probability[0] if len(probability) > 1 else 0, 4),
                "disponible": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error prediciendo dirección: {str(e)}")
            return {"error": str(e), "disponible": False}
    
    def predict_volatility(self, ticker: str, current_indicators: Dict) -> Dict[str, Any]:
        """
        Predice la volatilidad futura (ALTA/MEDIA/BAJA)
        
        Args:
            ticker: Símbolo del instrumento
            current_indicators: Dict con indicadores técnicos actuales
        
        Returns:
            Dict con predicción de volatilidad
        """
        try:
            if self.volatility_model is None:
                return {"error": "Modelo no entrenado", "disponible": False}
            
            # Extraer features
            features = self._extract_features_from_indicators(current_indicators)
            features_scaled = self.scaler.transform([features])
            
            # Predicción
            prediction = self.volatility_model.predict(features_scaled)[0]
            probability = self.volatility_model.predict_proba(features_scaled)[0]
            
            volatility_levels = ["BAJA", "MEDIA", "ALTA"]
            volatility = volatility_levels[prediction] if prediction < len(volatility_levels) else "MEDIA"
            confidence = float(max(probability))
            
            return {
                "ticker": ticker,
                "volatilidad_predicha": volatility,
                "confianza": round(confidence, 4),
                "nivel_predicho": prediction,
                "disponible": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error prediciendo volatilidad: {str(e)}")
            return {"error": str(e), "disponible": False}
    
    def predict_confidence(self, ticker: str, current_indicators: Dict) -> Dict[str, Any]:
        """
        Predice el nivel de confianza de la recomendación
        
        Args:
            ticker: Símbolo del instrumento
            current_indicators: Dict con indicadores técnicos actuales
        
        Returns:
            Dict con predicción de confianza
        """
        try:
            if self.confidence_model is None:
                return {"error": "Modelo no entrenado", "disponible": False}
            
            # Extraer features
            features = self._extract_features_from_indicators(current_indicators)
            features_scaled = self.scaler.transform([features])
            
            # Predicción
            prediction = self.confidence_model.predict(features_scaled)[0]
            probability = self.confidence_model.predict_proba(features_scaled)[0]
            
            confidence_levels = ["BAJA", "MODERADA", "ALTA"]
            confidence = confidence_levels[prediction] if prediction < len(confidence_levels) else "MODERADA"
            score = float(max(probability))
            
            return {
                "ticker": ticker,
                "confianza_predicha": confidence,
                "score_confianza": round(score, 4),
                "nivel_predicho": prediction,
                "disponible": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error prediciendo confianza: {str(e)}")
            return {"error": str(e), "disponible": False}
    
    def predict_analyst_accuracy(self, analyst_history: Dict) -> Dict[str, Any]:
        """
        Predice qué tan acertados serán los ratings de analistas
        
        Args:
            analyst_history: Histórico de ratings vs resultados reales
        
        Returns:
            Dict con predicción de accuracy
        """
        try:
            if not analyst_history:
                return {
                    "accuracy_esperada": 0.65,
                    "confianza": "BAJA",
                    "disponible": False,
                    "razon": "Histórico insuficiente"
                }
            
            # Calcular accuracy histórico
            correct = analyst_history.get("correct", 0)
            total = analyst_history.get("total", 1)
            accuracy = correct / total if total > 0 else 0.65
            
            # Estimar confianza basada en accuracy
            if accuracy > 0.70:
                confidence = "ALTA"
                expected = 0.75
            elif accuracy > 0.55:
                confidence = "MODERADA"
                expected = 0.65
            else:
                confidence = "BAJA"
                expected = 0.55
            
            return {
                "accuracy_historica": round(accuracy, 4),
                "accuracy_esperada": round(expected, 4),
                "confianza_analistas": confidence,
                "disponible": True,
                "muestras": total,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error prediciendo accuracy de analistas: {str(e)}")
            return {"error": str(e), "disponible": False}
    
    def _extract_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Extrae features de un DataFrame histórico"""
        try:
            if len(df) < 30:
                return None, None, None
            
            # Features de precio
            close = df['Close'].values
            returns = np.diff(close) / close[:-1]
            
            # Label: dirección próxima semana
            future_return = np.diff(close[5:]) / close[5:-1]  # 5 días después
            y_direction = (future_return > 0).astype(int)
            
            # Label: volatilidad
            rolling_vol = pd.Series(returns).rolling(20).std().values[20:]
            vol_median = np.median(rolling_vol[rolling_vol > 0])
            y_volatility = (rolling_vol > vol_median).astype(int)
            
            # Features: 20 características técnicas
            X = []
            for i in range(20, len(close) - 5):
                window = close[i-20:i]
                
                # Características básicas
                sma_10 = np.mean(window[-10:])
                sma_20 = np.mean(window)
                momentum = (window[-1] - window[0]) / window[0]
                volatility_window = np.std(np.diff(window) / window[:-1])
                rsi = self._calculate_rsi(window)
                
                # Más características
                high_low_ratio = np.max(window) / np.min(window)
                open_close_ratio = (window[-1] - window[0]) / window[0]
                acceleration = momentum / (np.std(np.diff(window)) + 0.0001)
                trend = (window[-1] > sma_10) and (sma_10 > sma_20)
                
                feature_row = [
                    momentum,
                    volatility_window,
                    rsi,
                    high_low_ratio,
                    open_close_ratio,
                    acceleration,
                    float(trend),
                    sma_10 / sma_20,
                    np.std(window),
                    np.mean(np.abs(np.diff(window))),
                ]
                
                # Pad to 20 features
                while len(feature_row) < 20:
                    feature_row.append(0)
                
                X.append(feature_row[:20])
            
            if len(X) < len(y_direction):
                X = X[:len(y_direction)]
            else:
                y_direction = y_direction[:len(X)]
                y_volatility = y_volatility[:len(X)]
            
            return np.array(X), y_direction, y_volatility
            
        except Exception as e:
            self.logger.warning(f"Error extrayendo features: {str(e)}")
            return None, None, None
    
    def _extract_features_from_indicators(self, indicators: Dict) -> np.ndarray:
        """Extrae features de dict de indicadores actuales"""
        features = []
        
        # RSI
        rsi = indicators.get("RSI", {}).get("valor", 50) / 100
        features.append(rsi)
        
        # MACD
        macd_val = indicators.get("MACD", {}).get("linea_macd", 0)
        features.append(macd_val / 100 if macd_val else 0)
        
        # Stochastic
        stoch_k = indicators.get("STOCHASTIC", {}).get("linea_k", 50) / 100
        features.append(stoch_k)
        
        # Medias móviles
        sma_20 = indicators.get("MEDIAS_MOVILES", {}).get("SMA_20", 0)
        sma_50 = indicators.get("MEDIAS_MOVILES", {}).get("SMA_50", 0)
        if sma_50:
            features.append(sma_20 / sma_50 if sma_20 else 1)
        else:
            features.append(0)
        
        # Volumen
        vol_rel = indicators.get("VOLUMEN", {}).get("relacion", 1)
        features.append(vol_rel / 2)  # Normalizar
        
        # Pad to 20 features
        while len(features) < 20:
            features.append(0)
        
        return np.array(features[:20])
    
    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> float:
        """Calcula RSI manualmente"""
        if len(prices) < period:
            return 50
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100 if avg_gain > 0 else 50
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_confidence_labels(self, X: np.ndarray) -> np.ndarray:
        """Calcula etiquetas de confianza basadas en features"""
        confidence_scores = []
        
        for features in X:
            # Calcula una puntuación de "consistencia"
            variance = np.var(features)
            mean = np.mean(features)
            
            if variance < 0.1:
                confidence = 2  # ALTA
            elif variance < 0.3:
                confidence = 1  # MODERADA
            else:
                confidence = 0  # BAJA
            
            confidence_scores.append(confidence)
        
        return np.array(confidence_scores)
    
    def _save_models(self):
        """Guarda los modelos entrenados"""
        try:
            models = {
                "price_direction": self.price_direction_model,
                "volatility": self.volatility_model,
                "confidence": self.confidence_model,
                "scaler": self.scaler
            }
            
            for name, model in models.items():
                if model:
                    path = os.path.join(self.model_dir, f"{name}_model.pkl")
                    with open(path, "wb") as f:
                        pickle.dump(model, f)
            
            self.logger.info("✅ Modelos guardados exitosamente")
            
        except Exception as e:
            self.logger.error(f"Error guardando modelos: {str(e)}")
    
    def _load_models(self):
        """Carga modelos previamente entrenados"""
        try:
            for name in ["price_direction", "volatility", "confidence"]:
                path = os.path.join(self.model_dir, f"{name}_model.pkl")
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        model = pickle.load(f)
                        if name == "price_direction":
                            self.price_direction_model = model
                        elif name == "volatility":
                            self.volatility_model = model
                        elif name == "confidence":
                            self.confidence_model = model
            
            # Cargar scaler
            scaler_path = os.path.join(self.model_dir, "scaler_model.pkl")
            if os.path.exists(scaler_path):
                with open(scaler_path, "rb") as f:
                    self.scaler = pickle.load(f)
            
            if self.price_direction_model:
                self.logger.info("✅ Modelos cargados exitosamente")
            
        except Exception as e:
            self.logger.warning(f"⚠️  No se pudieron cargar modelos: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene estado de los modelos"""
        return {
            "modulo": "MLPredictor",
            "price_direction_model": "✅ Disponible" if self.price_direction_model else "❌ No disponible",
            "volatility_model": "✅ Disponible" if self.volatility_model else "❌ No disponible",
            "confidence_model": "✅ Disponible" if self.confidence_model else "❌ No disponible",
            "estado": "✅ Operativo" if any([self.price_direction_model, self.volatility_model]) else "❌ Modelos no entrenados"
        }
