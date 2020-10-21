function makeSlider(id, when_changed) {
    // internal data
    let touched = false;
    let changed = false;
    let position = 0;
    const slider = $('#' + id);
    // internal functions
    const set_position = function(new_position) {
        position = Math.round(new_position);
        slider.find('.slider_tick')[0].setAttribute('cy', position);
        changed = true;
    };
    slider.on('touchmove', event => {
        let touch = event.targetTouches[0];
        // Get the touch relative to the top of the slider
        let from_top = touch.pageY - slider.offset().top;
        // Convert to twice a percentage of the track. (0 is the middle)
        let relative_touch = (from_top / slider.height()) * 200;
        set_position(relative_touch - 100);
        touched = true;
        event.preventDefault();
    });
    slider.on('touchend', () => touched = false);

    const update = function() {
        if(!touched && Math.abs(position) > 0) {
            // drift back to the middle - add 0.5 to the movement, in the right direction to round up to at least 1%
            let error = 0 - position;
            let change = (0.3 * error) + (Math.sign(error) * 0.5);
            set_position(position + change);
            // console.log(id + ": " + position);
        }
    };
    setInterval(update, 50);

    const update_if_changed = function() {
        if(changed) {
            changed = false;
            // Call the callback - invert the track so 'up' is positive
            when_changed(-position);
        }
    };
    setInterval(update_if_changed, 200);
}
