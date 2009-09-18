require "json"
require "haml"

contexts = JSON.parse(File.read(File.dirname(__FILE__) + "/tests.json"))

contexts.each do |context|
  context_name = context[0]
  expectations = context[1]
  describe "When handling #{context_name}," do
     expectations.each do |name, ex|
       it "should render \"#{name}\" as \"#{ex["html"]}\"" do
         locals = Hash[*(ex["locals"] || {}).collect {|k, v| [k.to_sym, v] }.flatten]
         options = Hash[*(ex["config"] || {}).collect {|k, v| [k.to_sym, v.to_sym] }.flatten]
         engine = Haml::Engine.new(ex["haml"], options)
         engine.render(Object.new, locals).chomp.should == ex["html"]
       end
     end
  end
end


