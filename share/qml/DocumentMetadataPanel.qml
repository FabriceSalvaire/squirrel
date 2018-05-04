/***************************************************************************************************
 *
 * Copyright (C) 2018 Fabrice Salvaire
 * Contact: http://www.fabrice-salvaire.fr
 *
 * This file is part of the Babel software.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 **************************************************************************************************/

import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.3

import Constants 1.0

Rectangle {
    id: document_metadata_panel

    // anchors.fill: parent

    color: application_style.window_color

    property var languages: application_style.languages

    function set_document(document) {
        title_text_area.text = document.title
        author_text_area.text = document.author
	star_count_wrapper.set_star_count(document.star)
	language_combobox.set_language(document.language_id)
        number_of_page.text = document.number_of_pages
        comment_area.text = document.comment
    }

    ColumnLayout {
	anchors.fill: parent
        anchors.margins: Style.spacing.base
        spacing: Style.spacing.base_vertical

        TextArea {
	    id: title_text_area
	    Layout.fillWidth: true
            implicitHeight: contentHeight * 1.1
            // placeholderText: qsTr('Enter title')
            // text: qsTr('Title ...') // Fixme: segfault
            text: 'Title ...'
        }

        RowLayout {
	    Layout.fillWidth: true
            spacing: Style.spacing.base_horizontal

            Text {
                Layout.alignment: Qt.AlignTop
                text: qsTr('Author')
            }

            TextArea {
		id: author_text_area
                Layout.alignment: Qt.AlignTop
                Layout.fillWidth: true
                implicitHeight: contentHeight * 1.1
                text: '...'
            }
	}

        RowLayout {
	    Layout.fillWidth: true
            spacing: Style.spacing.base_horizontal

            Text {
                text: qsTr('Star')
            }

	    Item {
		implicitWidth: childrenRect.width
		implicitHeight: childrenRect.height

		Row {
		    Repeater {
			id: star_count_wrapper
			readonly property int number_of_stars: 5
			model: number_of_stars

			Image {
			    property bool stared: false
			    source: 'qrc:/icons/36x36/' + (stared ? 'star-black.png' : 'star-border-black.png')
			}

			function set_star_count(star_count) {
			    for (var i = 0; i < number_of_stars; i++) {
				var star = star_count_wrapper.itemAt(i)
				star.stared = star_count ? i <= star_count : false
			    }
			}
		    }
		}

		MouseArea {
		    anchors.fill: parent
		    onPositionChanged: update_star_count(mouse)
		    onPressed: update_star_count(mouse)

		    function update_star_count(mouse) {
			var star_count = Math.ceil(mouse.x / parent.width * 5) -1
			star_count_wrapper.set_star_count(star_count)
		    }
		}
	    }
	}

        RowLayout {
	    Layout.fillWidth: true
            spacing: Style.spacing.base_horizontal

            Text {
                text: qsTr('Language')
            }

	    ComboBox {
		id: language_combobox
		model: languages

		function set_language(language_id) {
		    // var language_index = languages.findIndex(function(element) {
		    // 	return element == language;
		    // })
		    language_combobox.currentIndex = language_id
		}
	    }
	}

	RowLayout {
	    Layout.fillWidth: true
            spacing: Style.spacing.base_horizontal

            Text {
                text: qsTr('Number of pages')
            }

            Text {
		id: number_of_page
                text: '...'
            }
	}

	ColumnLayout {
	    Layout.fillWidth: true
            Text {
		Layout.fillWidth: true
                text: qsTr('Comment')
            }
	    TextArea {
		id: comment_area
		Layout.fillWidth: true
		implicitHeight: contentHeight * 1.1
		text: ''
            }
        }
    }
}
