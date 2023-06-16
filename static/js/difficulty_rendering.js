const difficulty_divs = document.getElementsByClassName('diff container-lg rounded-2')
        for (let i = 0; i < difficulty_divs.length; i++) {
            const level = parseInt(difficulty_divs[i].innerText.split('/')[0])
            const all_levels = parseInt(difficulty_divs[i].innerText.split('/')[1])

            const div_color = 'hsl(' + (100 - 100.0 / (all_levels - 1) * (level - 1)) + ', 55%, 70%)';
            const font_color = 'hsl(' + (100 - 100.0 / (all_levels - 1) * (level - 1)) + ', 85%, 95%)';
            difficulty_divs[i].style.backgroundColor = div_color;
            difficulty_divs[i].style.color = font_color;
        }