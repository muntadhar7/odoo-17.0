/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Playground extends Component {
    static template = "awesome_owl.playground";
     setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
    }
}
