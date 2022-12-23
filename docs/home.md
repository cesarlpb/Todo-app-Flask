# Sección home

- [clip-path](https://medium.com/code-manthra/triangle-using-css-clip-path-polygon-b358a0fa2e0e)
- [polygon](https://developer.mozilla.org/en-US/docs/Web/CSS/basic-shape/polygon)
- [clip-path](https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path)
- [CSS-Tricks clip-path](https://css-tricks.com/almanac/properties/c/clip-path/)
- [Más sobre clip-path](https://css-tricks.com/background-image-shapes/)

## Herramientas
- [Colores de imágenes](https://html-color-codes.info/colors-from-image/)
- [Generador de clip-path](https://bennettfeely.com/clippy/)

### Botones
- [Generador de botones](https://css3buttongenerator.com/)
- [CSS Botones](https://cssbuttongenerator.com/)

### Gradiente
- [Generador de gradiente](https://cssgradient.io/)
- [CSS Gradiente](https://cssgradient.io/gradient-backgrounds/)

```css
#home{
    background-image: linear-gradient(to right, #0FDBDB, #0875D8);
}
```

CSS para dar la forma triangular del diseño al `div`:
```css
#triangulo {
    margin: 0;
    padding: 0;
    height: 200px;
    display: block;
    width: 100;
    -webkit-clip-path: polygon(0% 0%, 0% 100%, 100% 100%);
    clip-path: polygon(0% 0%, 0% 100%, 100% 100%);
}
```

