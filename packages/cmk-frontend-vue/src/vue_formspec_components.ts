/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type VueSchema =
  | VueInteger
  | VueFloat
  | VueString
  | VueDictionary
  | VueList
  | VueSingleChoice
  | VueCascadingSingleChoice
  | VueLegacyValuespec

export type VueInteger = VueInteger1 & {
  vue_type?: 'integer'
  label?: string
  unit?: string
}
export type VueInteger1 = VueBase

export interface VueSingleChoiceElement {
  name: string
  title: string
}

export type VueSingleChoice = VueSingleChoice1 & {
  vue_type?: 'single_choice'
  label?: string
  unit?: string
  elements: VueSingleChoiceElement[]
}
export type VueSingleChoice1 = VueBase

export interface VueCascadingSingleChoiceElement {
  name: string
  title: string
  default_value: unknown
  parameter_form: VueSchema
}

export type VueCascadingSingleChoice = VueCascadingSingleChoice1 & {
  vue_type?: 'cascading_single_choice'
  elements: VueCascadingSingleChoiceElement[]
}
export type VueCascadingSingleChoice1 = VueBase

export type VueFloat = VueFloat1 & {
  vue_type?: 'float'
  label?: string
  unit?: string
}
export type VueFloat1 = VueBase
export type VueString = VueString1 & {
  vue_type?: 'text'
  placeholder?: string
}
export type VueString1 = VueBase
export type VueDictionary = VueDictionary1 & {
  vue_type?: 'dictionary'
  elements: VueDictionaryElement[]
}
export type VueDictionary1 = VueBase
export type VueList = VueList1 & {
  vue_type?: 'list'
  add_text?: string
  vue_schema?: VueSchema
}
export type VueList1 = VueBase
export type VueLegacyValuespec = VueLegacyValuespec1 & {
  vue_type?: 'legacy_valuespec'
}
export type VueLegacyValuespec1 = VueBase

export interface VueFormspecComponents {
  all_schemas?: VueSchema[]
}
export interface VueBase {
  title: string
  help: string
  validators?: {}[]
}
export interface VueDictionaryElement {
  ident: string
  required: boolean
  default_value: unknown
  vue_schema: VueSchema
}
