import React, { PureComponent } from "react";
import PropTypes from "prop-types";
import "./EmojiResultRow.css";

export default class EmojiResultsRow extends PureComponent {
  static propTypes = {
    title: PropTypes.string,
  };

  render() {
    
    
    return (
      <div
        className="component-emoji-result-row copy-to-clipboard"
        >
        <span className="title">{this.props.title}</span>
             </div>
    );
  }
}
