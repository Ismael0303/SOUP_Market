// Utilidades para lazy loading y optimización de rendimiento
import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';

// Lazy loading de componentes
export const lazyLoadComponent = (importFunc, fallback = null) => {
  const LazyComponent = React.lazy(importFunc);
  
  return (props) => (
    <React.Suspense fallback={fallback || <div className="flex items-center justify-center p-4">Cargando...</div>}>
      <LazyComponent {...props} />
    </React.Suspense>
  );
};

// Lazy loading de imágenes
export const lazyLoadImage = (src, placeholder = "https://placehold.co/400x250/007bff/ffffff?text=Cargando...") => {
  const [imageSrc, setImageSrc] = useState(placeholder);
  const [imageRef, setImageRef] = useState();

  useEffect(() => {
    let observer;
    let didCancel = false;

    if (imageRef && imageSrc === placeholder) {
      if (IntersectionObserver) {
        observer = new IntersectionObserver(
          entries => {
            entries.forEach(entry => {
              if (
                !didCancel &&
                (entry.intersectionRatio > 0 || entry.isIntersecting)
              ) {
                setImageSrc(src);
                observer.unobserve(imageRef);
              }
            });
          },
          {
            threshold: 0.01,
            rootMargin: "75%"
          }
        );
        observer.observe(imageRef);
      } else {
        // Fallback para navegadores que no soportan IntersectionObserver
        setImageSrc(src);
      }
    }
    return () => {
      didCancel = true;
      if (observer && observer.unobserve) {
        observer.unobserve(imageRef);
      }
    };
  }, [src, imageSrc, imageRef]);

  return [imageSrc, setImageRef];
};

// Debounce para optimizar búsquedas
export const useDebounce = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

// Throttle para optimizar eventos
export const useThrottle = (value, limit) => {
  const [throttledValue, setThrottledValue] = useState(value);
  const lastRan = useRef(Date.now());

  useEffect(() => {
    const handler = setTimeout(function() {
      if (Date.now() - lastRan.current >= limit) {
        setThrottledValue(value);
        lastRan.current = Date.now();
      }
    }, limit - (Date.now() - lastRan.current));

    return () => {
      clearTimeout(handler);
    };
  }, [value, limit]);

  return throttledValue;
};

// Memoización de listas largas
export const useMemoizedList = (list, dependencies = []) => {
  return useMemo(() => {
    return list;
  }, dependencies);
};

// Optimización de re-renders con React.memo
export const memoizedComponent = (Component, propsAreEqual) => {
  return React.memo(Component, propsAreEqual);
};

// Virtualización para listas largas
export const useVirtualization = (items, itemHeight, containerHeight) => {
  const [scrollTop, setScrollTop] = useState(0);
  
  const visibleItems = useMemo(() => {
    const startIndex = Math.floor(scrollTop / itemHeight);
    const endIndex = Math.min(
      startIndex + Math.ceil(containerHeight / itemHeight) + 1,
      items.length
    );
    
    return items.slice(startIndex, endIndex).map((item, index) => ({
      ...item,
      index: startIndex + index,
      style: {
        position: 'absolute',
        top: (startIndex + index) * itemHeight,
        height: itemHeight,
        width: '100%'
      }
    }));
  }, [items, itemHeight, containerHeight, scrollTop]);

  const totalHeight = items.length * itemHeight;

  return {
    visibleItems,
    totalHeight,
    onScroll: (e) => setScrollTop(e.target.scrollTop)
  };
};

// Preload de recursos críticos
export const preloadResource = (href, as = 'script') => {
  const link = document.createElement('link');
  link.rel = 'preload';
  link.href = href;
  link.as = as;
  document.head.appendChild(link);
};

// Prefetch de rutas
export const prefetchRoute = (path) => {
  const link = document.createElement('link');
  link.rel = 'prefetch';
  link.href = path;
  document.head.appendChild(link);
};

// Optimización de imágenes
export const optimizeImage = (src, width, quality = 80) => {
  // Aquí podrías integrar con servicios como Cloudinary, ImageKit, etc.
  // Por ahora retornamos la URL original
  return src;
};

// Cache de datos
export const useCache = (key, fetcher, ttl = 5 * 60 * 1000) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    // Verificar cache
    const cached = localStorage.getItem(`cache_${key}`);
    if (cached) {
      const { data: cachedData, timestamp } = JSON.parse(cached);
      if (Date.now() - timestamp < ttl) {
        setData(cachedData);
        return;
      }
    }

    setLoading(true);
    setError(null);

    try {
      const result = await fetcher();
      setData(result);
      
      // Guardar en cache
      localStorage.setItem(`cache_${key}`, JSON.stringify({
        data: result,
        timestamp: Date.now()
      }));
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [key, fetcher, ttl]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}; 