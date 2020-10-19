function Slider(id, when_updated) {
    this.selector = '#' + id;
    this.when_updated = when_updated;
}

Slider.prototype = {
    touched: false, // is a touch still occuring
    touchmove: function(event) {
        let touch = event.targetTouches[0];
        // Get the touch relative to the top of the slider
        let from_top = touch.pageY - $(this.selector).offset().top;
        // height of track in pixels
        let trackheight = $(this.selector).height();
        // Convert this to twice a percentage of the track. (0 is the middle)
        let relative_touch = (from_top / trackheight) * 100;
        this.set_position(relative_touch);
        this.touched = true;
        event.preventDefault();
    },
    touchend: function(event) {
        this.touched = false;
    },
    setup: function() {
        $(this.selector).on('touchmove', this.touchmove.bind(this));
        $(this.selector).on('touchend', this.touchend.bind(this));
        setInterval(this.update.bind(this), 50);
        setInterval(this.update_if_changed.bind(this), 200);
    },
    changed: false,
    position : 50,
    set_position: function(new_position) {
        this.position = Math.round(new_position);
        console.log(this.id + " - " + this.position);
        $(this.selector).find('.slider_tick')[0].setAttribute('cy', this.position + '%');
        this.changed = true;
    },
    update: function() {
        let error = 50 - this.position;
        let change = (0.3 * error) + (Math.sign(error) * 0.5);
        if(!this.touched && this.position != 50) {
            this.set_position(this.position + change);
        }
    },
    update_if_changed: function() {
        if(this.changed) {
            this.changed = false;
            this.when_updated(100 - this.position * 2);
        }
    }
};
